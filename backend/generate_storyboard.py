import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

print("===== STORYBOARD GENERATOR (COLAB VERSION) =====")

RAG_OUTPUT_FILE = "rag_output.txt"
DATA_FOLDER = "data"


def read_rag_output():
    if not os.path.exists(RAG_OUTPUT_FILE):
        print("❌ rag_output.txt not found")
        return None

    with open(RAG_OUTPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        print("❌ rag_output.txt is empty")
        return None

    return content


def load_llm():
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    device = 0 if torch.cuda.is_available() else -1

    pipe = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        device=device,
        max_new_tokens=1500,
        temperature=0.3,
        do_sample=False
    )

    return pipe


def generate_storyboard(project_text):

    llm = load_llm()

    prompt = f"""
Create EXACTLY 15 scenes storyboard.

Each scene must have:

Scene X — Title
Narration:
4-6 sentences explanation.

Visual:
Detailed image generation prompt.

Project:
{project_text}
"""

    response = llm(prompt)[0]["generated_text"]
    return response


def save_files(storyboard):

    os.makedirs(DATA_FOLDER, exist_ok=True)

    storyboard_path = os.path.join(DATA_FOLDER, "storyboard.txt")
    narration_path = os.path.join(DATA_FOLDER, "narration.txt")
    visual_path = os.path.join(DATA_FOLDER, "visual_prompts.txt")

    with open(storyboard_path, "w", encoding="utf-8") as f:
        f.write(storyboard)

    narrations = re.findall(
        r"Narration:\s*(.*?)(?=\nVisual:)",
        storyboard,
        re.DOTALL
    )

    with open(narration_path, "w", encoding="utf-8") as f:
        for i, text in enumerate(narrations, start=1):
            f.write(f"Scene {i}:\n{text.strip()}\n\n")

    visuals = re.findall(
        r"Visual:\s*(.*?)(?=\nScene|\Z)",
        storyboard,
        re.DOTALL
    )

    with open(visual_path, "w", encoding="utf-8") as f:
        for i, text in enumerate(visuals, start=1):
            f.write(f"Scene {i}: {text.strip()}\n\n")

    print("✅ storyboard.txt, narration.txt, visual_prompts.txt saved")


if __name__ == "__main__":

    project_text = read_rag_output()

    if not project_text:
        exit()

    result = generate_storyboard(project_text)

    print(result)

    save_files(result)