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

# Faster but still accurate
OLLAMA_MODEL = "mistral:7b-instruct"


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

    print("✅ Old outputs cleared")


# ==============================
# LOAD MODEL
# ==============================

def load_llm():

    print("🔄 Loading Ollama model...\n")

    return OllamaLLM(
        model=OLLAMA_MODEL,
        temperature=0,
        num_predict=1500   # enough tokens for 15 scenes
    )


# ==============================
# READ PROJECT INPUT
# ==============================

def read_project_input():

    if not os.path.exists(RAG_OUTPUT_FILE):
        print("❌ rag_output.txt not found")
        return None

    with open(RAG_OUTPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if len(text) == 0:
        print("❌ rag_output.txt is empty")
        return None

    return text


# ==============================
# GENERATE STORYBOARD
# ==============================

def generate_storyboard(project_text, llm):

    print("\n🎬 Generating Storyboard...\n")

    prompt = f"""

You are an expert AI explainer video storyboard generator.

Convert the project documentation below into a structured storyboard.

STRICT RULES:

1. Generate EXACTLY 15 scenes.
2. Each scene must explain a step of the system.
3. Each narration must contain 3 sentences.
4. Do not change the project topic.
5. Do not add extra explanations.

FORMAT STRICTLY LIKE THIS:

Scene 1
Title: Short title

Narration:
3 clear sentences explaining the concept.

Visual Prompt:
A detailed realistic description for image generation.

Continue the same structure until Scene 15.

PROJECT DESCRIPTION:
{project_text}

Return ONLY the scenes.
"""

    response = llm.invoke(prompt)

    return response


# ==============================
# SAVE OUTPUTS
# ==============================

def save_outputs(text):

    print("💾 Saving outputs...\n")

    with open(STORYBOARD_FILE, "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ storyboard.txt saved")


    # --------------------------
    # Extract scenes
    # --------------------------

    scenes = re.split(r"Scene\s+\d+", text)
    scenes = [s.strip() for s in scenes if s.strip()]

    narrations = []
    visuals = []

    for scene in scenes:

        narration_match = re.search(
            r"Narration:\s*(.*?)\s*Visual Prompt:",
            scene,
            re.DOTALL
        )

        visual_match = re.search(
            r"Visual Prompt:\s*(.*)",
            scene,
            re.DOTALL
        )

        if narration_match:
            narrations.append(narration_match.group(1).strip())

        if visual_match:
            visuals.append(visual_match.group(1).strip())


    # --------------------------
    # SAVE NARRATIONS
    # --------------------------

    with open(NARRATION_FILE, "w", encoding="utf-8") as f:

        for i, n in enumerate(narrations, 1):
            f.write(f"Scene {i}\n\n")
            f.write(n)
            f.write("\n\n")

    print("✅ narration.txt saved")


    # --------------------------
    # SAVE VISUAL PROMPTS
    # --------------------------

    with open(VISUAL_FILE, "w", encoding="utf-8") as f:

        for i, v in enumerate(visuals, 1):
            f.write(f"Scene {i}\n\n")
            f.write(v)
            f.write("\n\n")

    print("✅ visual_prompts.txt saved")


    print("\n📊 Summary:")
    print("Narrations:", len(narrations))
    print("Visual Prompts:", len(visuals))


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("\n==============================")
    print("🎬 AI STORYBOARD GENERATOR")
    print("==============================\n")

    ensure_data_folder()

    clear_old_outputs()

    project_text = read_project_input()

    if project_text is None:
        exit()

    llm = load_llm()

    storyboard = generate_storyboard(project_text, llm)

    save_outputs(storyboard)

    print("\n🎬 STORYBOARD COMPLETE!")
    print("📁 Check folder: data/")