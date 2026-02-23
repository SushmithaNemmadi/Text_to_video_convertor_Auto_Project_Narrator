import fitz
import ollama
import re
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==============================
# SETTINGS
# ==============================

PDF_PATH = "dataset/projects.pdf"
MODEL_NAME = "llama3:8b"
OUTPUT_FILE = "project_knowledge.json"
MAX_WORKERS = 2   # Reduce to 1 if laptop heats


# ==============================
# STEP 1 — Extract Project Titles
# ==============================

def extract_titles(pdf_path):
    print("Extracting project titles from PDF...")

    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    matches = re.findall(r"\d+\.\s*(.+)|\n\d+\s+([A-Za-z].+)", text)

    titles = []
    for m in matches:
        title = m[0] if m[0] else m[1]
        if title:
            titles.append(title.strip())

    titles = list(set(titles))  # remove duplicates

    print("Total titles found:", len(titles))
    return titles


# ==============================
# STEP 2 — Generate Project Info
# ==============================

def generate_project_info(title, retries=3):

    prompt = f"""
Generate software project documentation.

Project Title: {title}

Return structured output EXACTLY in this format:

Project Overview:
Objective:
Domain:
Software Requirements:
Hardware Requirements:
Workflow:
System Architecture:
Input:
Output:
Implementation Steps:
Benefits:
Future Scope:

Rules:
- No diagrams
- Be technically realistic
- Keep response under 300 words
"""

    for attempt in range(retries):
        try:
            print("Generating:", title)

            response = ollama.chat(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.2}
            )

            return {
                "title": title,
                "documentation": response["message"]["content"]
            }

        except Exception:
            print(f"Retry {attempt+1} for {title}")
            time.sleep(3)

    print("FAILED:", title)
    return {"title": title, "documentation": "FAILED"}


# ==============================
# STEP 3 — Resume-Safe Processing
# ==============================

def process_all_projects(titles):

    # Load existing data if available
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing_results = json.load(f)
    else:
        existing_results = []

    # Extract completed titles
    completed_titles = {item["title"] for item in existing_results}

    # Filter remaining titles
    remaining_titles = [t for t in titles if t not in completed_titles]

    print(f"\nAlready completed: {len(completed_titles)}")
    print(f"Remaining to generate: {len(remaining_titles)}\n")

    results = existing_results.copy()

    if not remaining_titles:
        print("All projects already generated ✅")
        return results

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(generate_project_info, t) for t in remaining_titles]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            # Save after each completed project (very important)
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)

    return results


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("Starting pipeline...\n")

    titles = extract_titles(PDF_PATH)

    print("\nGenerating project documentation using Ollama...\n")

    results = process_all_projects(titles)

    print("\nDone!")
    print("Saved to:", OUTPUT_FILE)