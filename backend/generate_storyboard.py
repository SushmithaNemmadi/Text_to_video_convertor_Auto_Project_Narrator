import ollama
import os
import re

print("===== STORYBOARD GENERATOR (15 SCENES WITH VISUAL PROMPTS) =====")

# ==============================
# SETTINGS
# ==============================

RAG_OUTPUT_FILE = "rag_output.txt"
DATA_FOLDER = "data"


# ==============================
# READ RAG OUTPUT
# ==============================

def read_rag_output():

    if not os.path.exists(RAG_OUTPUT_FILE):
        print("❌ rag_output.txt not found")
        return None

    with open(RAG_OUTPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        print("❌ rag_output.txt is empty")
        return None

    print("✅ Loaded project content from rag_output.txt")
    return content


# ==============================
# GENERATE STORYBOARD (15 SCENES)
# ==============================

def generate_storyboard(project_text):

    prompt = f"""
You are a professional technical explainer storyboard writer.

Convert the project documentation into a structured educational storyboard.

STRICT RULES (VERY IMPORTANT):
1. Generate EXACTLY 15 scenes.
2. Every scene MUST contain:
   - Scene title
   - Narration (4–6 sentences)
   - Visual prompt
3. Visual MUST NEVER be empty.
4. Visual must describe a detailed image generation prompt.
5. Visual must include diagrams, UI screens, workflow diagrams, architecture, or technical illustrations.
6. Explain ALL project information clearly.
7. Do NOT skip any details.

SCENE FLOW:
1. Project Overview
2. Problem Statement
3. Need for Solution
4. Project Objective
5. Domain Explanation
6. System Architecture
7. Components Explanation
8. Workflow Step 1
9. Workflow Step 2
10. Input and Output
11. Software Requirements
12. Hardware Requirements
13. Implementation Steps
14. Benefits and Applications
15. Future Scope and Conclusion

FORMAT STRICTLY:

Scene 1 — <Scene Title>
Narration:
<detailed explanation>

Visual:
<image generation prompt>

Scene 2 — <Scene Title>
Narration:
Visual:

Continue until Scene 15.

Project Description:
{project_text}
"""

    response = ollama.chat(
        model="mistral:7b-instruct-q4_0",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


# ==============================
# SAVE OUTPUT FILES
# ==============================

def save_files(storyboard):

    os.makedirs(DATA_FOLDER, exist_ok=True)

    storyboard_path = os.path.join(DATA_FOLDER, "storyboard.txt")
    narration_path = os.path.join(DATA_FOLDER, "narration.txt")
    visual_path = os.path.join(DATA_FOLDER, "visual_prompts.txt")

    # overwrite old files
    open(storyboard_path, "w").close()
    open(narration_path, "w").close()
    open(visual_path, "w").close()

    # ----------------------------
    # save full storyboard
    # ----------------------------
    with open(storyboard_path, "w", encoding="utf-8") as f:
        f.write(storyboard)

    # ----------------------------
    # extract narration blocks
    # ----------------------------
    narrations = re.findall(
        r"Narration:\s*(.*?)\n\s*Visual:",
        storyboard,
        re.DOTALL | re.IGNORECASE
    )

    with open(narration_path, "w", encoding="utf-8") as f:
        for i, text in enumerate(narrations, start=1):
            f.write(f"Scene {i}:\n{text.strip()}\n\n")

    # ----------------------------
    # extract visual prompts (robust)
    # ----------------------------
    visuals = re.findall(r"Visual:\s*(.*?)(?=\n\s*Scene|\Z)", storyboard, re.DOTALL)

    with open(visual_path, "w", encoding="utf-8") as f:
        for i in range(1, 16):

            try:
                visual_text = visuals[i - 1].strip()
            except:
                visual_text = ""

            # fallback if model fails
            if not visual_text:
                visual_text = (
                    f"high quality technical illustration of scene {i}, "
                    "software system workflow diagram, clean UI interface, "
                    "professional infographic style, white background"
                )

            f.write(f"Scene {i}: {visual_text}\n\n")

    print("\n✅ storyboard.txt saved")
    print("✅ narration.txt saved")
    print("✅ visual_prompts.txt saved")


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    project_text = read_rag_output()

    if not project_text:
        exit()

    print("\nGenerating 15-scene structured storyboard...\n")

    result = generate_storyboard(project_text)

    print("\n========== GENERATED STORYBOARD ==========\n")
    print(result)

    save_files(result)