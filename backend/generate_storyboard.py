import os
from langchain_ollama import OllamaLLM

# ==============================
# SETTINGS
# ==============================

INPUT_FILE = "rag_output.txt"
OUTPUT_FILE = "visual_prompts.txt"

OLLAMA_MODEL = "phi3:mini"


# ==============================
# LOAD MODEL
# ==============================

def load_llm():

    print("Loading Ollama model...")

    return OllamaLLM(
        model=OLLAMA_MODEL,
        temperature=0,
        num_predict=60
    )


# ==============================
# READ PROJECT TEXT
# ==============================

def read_input():

    if not os.path.exists(INPUT_FILE):
        print("rag_output.txt not found")
        return None

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


# ==============================
# GENERATE ONE VISUAL PROMPT
# ==============================

def generate_visual_prompt(scene_number, project_text, llm):

    prompt = f"""
Create ONE visual prompt for an educational YouTube tech explainer video.

Project:
{project_text}

Scene number: {scene_number}

RULES
- The image must explain the system visually
- Use system diagrams, workflows, or UI screens
- Avoid cinematic scenes or people typing

FORMAT
Visual Prompt:
"""

    result = llm.invoke(prompt)

    return f"Scene {scene_number}\n{result.strip()}\n"


# ==============================
# GENERATE 10 PROMPTS
# ==============================

def generate_prompts(project_text, llm):

    prompts = ""

    for i in range(1, 11):

        print(f"Generating visual prompt {i}")

        scene_prompt = generate_visual_prompt(i, project_text, llm)

        prompts += scene_prompt + "\n"

    return prompts


# ==============================
# SAVE OUTPUT
# ==============================

def save_output(prompts):

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(prompts)

    print("Saved visual prompts to", OUTPUT_FILE)


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("\nFAST VISUAL PROMPT GENERATOR\n")

    text = read_input()

    if text is None:
        exit()

    llm = load_llm()

    prompts = generate_prompts(text, llm)

    save_output(prompts)

    print("\nFinished generating 10 visual prompts.")