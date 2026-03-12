import os
import re
from langchain_ollama import OllamaLLM

# ==============================
# SETTINGS
# ==============================

INPUT_FILE = "rag_output.txt"

DATA_FOLDER = "data"
STORYBOARD_FILE = os.path.join(DATA_FOLDER, "storyboard.txt")
NARRATION_FILE = os.path.join(DATA_FOLDER, "narration.txt")
VISUAL_FILE = os.path.join(DATA_FOLDER, "visual_prompts.txt")

OLLAMA_MODEL = "phi3:mini"
TOTAL_SCENES = 10


# ==============================
# LOAD MODEL
# ==============================

def load_llm():

    print("Loading Ollama model...")

    return OllamaLLM(
        model=OLLAMA_MODEL,
        temperature=0,
        num_predict=1200
    )


# ==============================
# READ PROJECT TEXT
# ==============================

def read_project():

    if not os.path.exists(INPUT_FILE):
        print("rag_output.txt not found")
        return None

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


# ==============================
# GENERATE STORYBOARD
# ==============================

def generate_storyboard(project_text, llm):

    prompt = f"""
You are creating a storyboard for a technical YouTube explainer video.

Project description:
{project_text}

You MUST create exactly {TOTAL_SCENES} scenes.

IMPORTANT RULES:
- Do NOT generate fewer than {TOTAL_SCENES} scenes
- Do NOT generate more than {TOTAL_SCENES} scenes
- Each scene must explain a different part of the system

STRICT FORMAT:

Scene 1
Narration: ...
Visual: ...

Scene 2
Narration: ...
Visual: ...

Continue until Scene {TOTAL_SCENES}.
"""

    result = llm.invoke(prompt)

    return result.strip()


# ==============================
# PARSE STORYBOARD
# ==============================

def parse_storyboard(storyboard):

    narration_list = []
    visual_list = []

    scenes = re.split(r"Scene\s+\d+", storyboard)

    scene_number = 1

    for scene in scenes:

        if scene.strip() == "":
            continue

        narration_match = re.search(r"Narration:\s*(.*)", scene)
        visual_match = re.search(r"Visual:\s*(.*)", scene)

        if narration_match:
            narration_text = narration_match.group(1).strip()
            narration_list.append(f"Scene {scene_number}\n{narration_text}")

        if visual_match:
            visual_text = visual_match.group(1).strip()
            visual_list.append(f"Scene {scene_number}\n{visual_text}")

        scene_number += 1

    return narration_list, visual_list


# ==============================
# SAVE FILE
# ==============================

def save_file(path, content):

    with open(path, "w", encoding="utf-8") as f:

        if isinstance(content, list):
            f.write("\n\n".join(content))
        else:
            f.write(content)

    print("Saved:", path)


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("\nAI STORYBOARD GENERATOR\n")

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    project_text = read_project()

    if project_text is None:
        exit()

    llm = load_llm()

    print("\nGenerating storyboard...\n")

    storyboard = generate_storyboard(project_text, llm)

    save_file(STORYBOARD_FILE, storyboard)

    print("\nExtracting narration and visuals...\n")

    narration, visuals = parse_storyboard(storyboard)

    save_file(NARRATION_FILE, narration)
    save_file(VISUAL_FILE, visuals)

    print("\nFinished generating files.")