import os
import re
from langchain_ollama import OllamaLLM

# ==============================
# SETTINGS
# ==============================

RAG_OUTPUT_FILE = "rag_output.txt"

DATA_FOLDER = "data"

STORYBOARD_FILE = os.path.join(DATA_FOLDER, "storyboard.txt")
NARRATION_FILE = os.path.join(DATA_FOLDER, "narration.txt")
VISUAL_FILE = os.path.join(DATA_FOLDER, "visual_prompts.txt")

OLLAMA_MODEL = "llama3:8b"


# ==============================
# CREATE DATA FOLDER
# ==============================

def ensure_data_folder():
    os.makedirs(DATA_FOLDER, exist_ok=True)


# ==============================
# CLEAR OLD OUTPUTS
# ==============================

def clear_old_outputs():

    open(STORYBOARD_FILE, "w").close()
    open(NARRATION_FILE, "w").close()
    open(VISUAL_FILE, "w").close()

    print("Old outputs cleared")


# ==============================
# LOAD MODEL
# ==============================

def load_llm():

    print("Loading Ollama model...\n")

    return OllamaLLM(
        model=OLLAMA_MODEL,
        temperature=0
    )


# ==============================
# READ PROJECT INPUT
# ==============================

def read_project_input():

    if not os.path.exists(RAG_OUTPUT_FILE):
        print("rag_output.txt not found")
        return None

    with open(RAG_OUTPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if len(text) == 0:
        print("rag_output.txt is empty")
        return None

    return text


# ==============================
# GENERATE STORYBOARD
# ==============================

def generate_storyboard(project_text, llm):

    print("\nGenerating Storyboard...\n")

    prompt = f"""

You are an expert AI video storyboard generator.

Convert the project description into a storyboard for an educational explainer video.

STRICT RULES

1. Generate EXACTLY 15 scenes.
2. Each scene must explain the system step-by-step.
3. Narration must contain 3-4 sentences.
4. Do NOT change the project topic.
5. Do NOT invent unrelated systems.

VISUAL PROMPT RULES (VERY IMPORTANT)

Images must contain NO TEXT.

Do NOT include:
- letters
- numbers
- captions
- UI text
- dashboards
- charts
- diagrams with labels
- titles
- subtitles

Images must be:
- cinematic
- realistic
- detailed
- visually descriptive
- suitable for AI image generation

FORMAT EXACTLY LIKE THIS:

Scene 1
Title: Short title

Narration:
3-4 sentences explaining the concept.

Visual Prompt:
A cinematic realistic scene with NO text, NO letters, NO numbers.

Continue the same structure until Scene 15.

PROJECT DESCRIPTION:
{project_text}

Return ONLY the scenes.

"""

    response = llm.invoke(prompt)

    return response


# ==============================
# EXTRACT DATA
# ==============================

def extract_data(storyboard):

    scenes = re.split(r"Scene\s*\d+", storyboard)

    narrations = []
    visuals = []

    for scene in scenes:

        if "Narration" not in scene:
            continue

        narration_match = re.search(
            r"Narration:\s*(.*?)\s*Visual Prompt:",
            scene,
            re.DOTALL | re.IGNORECASE
        )

        visual_match = re.search(
            r"Visual Prompt:\s*(.*)",
            scene,
            re.DOTALL | re.IGNORECASE
        )

        if narration_match:
            narrations.append(narration_match.group(1).strip())

        if visual_match:
            visuals.append(visual_match.group(1).strip())

    return narrations, visuals


# ==============================
# SAVE OUTPUTS
# ==============================

def save_outputs(storyboard):

    print("Saving outputs...\n")

    with open(STORYBOARD_FILE, "w", encoding="utf-8") as f:
        f.write(storyboard)

    print("storyboard.txt saved")

    narrations, visuals = extract_data(storyboard)

    if len(narrations) == 0:
        print("Narrations not detected. Check LLM format.")

    if len(visuals) == 0:
        print("Visual prompts not detected. Check LLM format.")

    # SAVE NARRATIONS
    with open(NARRATION_FILE, "w", encoding="utf-8") as f:

        for i, n in enumerate(narrations, 1):

            f.write(f"Scene {i}\n\n")
            f.write(n)
            f.write("\n\n")

    print("narration.txt saved")

    # SAVE VISUAL PROMPTS
    with open(VISUAL_FILE, "w", encoding="utf-8") as f:

        for i, v in enumerate(visuals, 1):

            f.write(f"Scene {i}\n\n")
            f.write(v)
            f.write("\n\n")

    print("visual_prompts.txt saved")

    print("\nSummary:")
    print("Narrations:", len(narrations))
    print("Visual Prompts:", len(visuals))


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("\n==============================")
    print("AI STORYBOARD GENERATOR")
    print("==============================\n")

    ensure_data_folder()

    clear_old_outputs()

    project_text = read_project_input()

    if project_text is None:
        exit()

    llm = load_llm()

    storyboard = generate_storyboard(project_text, llm)

    save_outputs(storyboard)

    print("\nSTORYBOARD COMPLETE!")
    print("Check folder: data/")