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
        num_predict=700
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
# COUNT SCENES
# ==============================

def count_scenes(text):
    return len(re.findall(r"Scene\s+\d+", text))


# ==============================
# GENERATE STORYBOARD
# ==============================

def generate_storyboard(project_text, llm):

    prompt = f"""
Create a storyboard for a YouTube educational explainer video.

Project description:
{project_text}

IMPORTANT:
You MUST generate EXACTLY {TOTAL_SCENES} scenes.

Do NOT generate more or less than {TOTAL_SCENES} scenes.

Scene structure MUST follow:

Scene 1 → What is the project (overview)

Scene 2 → Why the project is needed (problem + purpose)

Scene 3 → How the system works (workflow diagram)

Scene 4 → How to start building the project

Scene 5 → Information/data required for the project

Scene 6 → Software requirements

Scene 7 → Hardware requirements

Scene 8 → System inputs

Scene 9 → System outputs

Scene 10 → Benefits and final conclusion

RULES:

• Narration must be short (1–2 sentences)
• Visual must describe an educational infographic or diagram
• Each visual must be completely different
• Avoid developer coding scenes
• Output MUST stop after Scene 10

STRICT FORMAT:

Scene 1
Narration: ...
Visual: ...

Scene 2
Narration: ...
Visual: ...

Continue until Scene 10 only.
"""

    # retry until correct scenes
    for attempt in range(3):

        print(f"Generating storyboard attempt {attempt+1}...")

        result = llm.invoke(prompt).strip()

        scene_count = count_scenes(result)

        if scene_count == TOTAL_SCENES:
            print("Correct number of scenes generated.")
            return result

        print(f"Generated {scene_count} scenes. Retrying...\n")

    # fallback: trim extra scenes
    scenes = re.split(r"(Scene\s+\d+)", result)

    final_text = ""
    scene_counter = 0

    for i in range(1, len(scenes), 2):

        scene_counter += 1

        if scene_counter > TOTAL_SCENES:
            break

        final_text += scenes[i] + scenes[i+1]

    return final_text.strip()


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