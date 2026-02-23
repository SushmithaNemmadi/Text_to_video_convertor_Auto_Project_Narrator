import pdfplumber
import re
import json
import os

# ✅ CHANGE PATH (based on your folder structure)
pdf_path = "dataset/projects.pdf"   # put your pdf in dataset folder
output_file = "dataset/project_training.jsonl"

projects = []

# check if file exists
if not os.path.exists(pdf_path):
    print(f"❌ PDF not found: {pdf_path}")
    exit()

print("📄 Reading PDF...")

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()

        if not text:
            continue

        lines = text.split("\n")

        for line in lines:
            line = line.strip()

            # skip empty lines
            if not line:
                continue

            # ✅ match numbered project titles like:
            # 1. Project Name
            # 1011.Project Name
            # 300. Project Name
            match = re.match(r"^\d+\.\s*(.+)", line)

            if match:
                project_name = match.group(1).strip()

                # skip garbage lines
                if len(project_name) < 3:
                    continue

                # generate storyboard output
                output = (
                    f"Project Overview: System for {project_name.lower()}. "
                    f"Objective: Improve efficiency and performance in {project_name.lower()}. "
                    f"Workflow: Data collection → processing → analysis → result generation. "
                    f"Software Requirements: Python, Database. "
                    f"Hardware Requirements: Computer system."
                )

                projects.append({
                    "instruction": "Generate project storyboard",
                    "input": project_name,
                    "output": output
                })

# remove duplicates
unique_projects = {p["input"]: p for p in projects}.values()

# save jsonl
with open(output_file, "w", encoding="utf-8") as f:
    for item in unique_projects:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"✅ Generated {len(unique_projects)} entries")
print(f"📁 Saved to: {output_file}")