import json
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
SCENES_JSON_FILE = os.path.join(DATA_FOLDER, "scenes.json")

OLLAMA_MODEL = "llama3:8b"

# ==============================
# CREATE DATA FOLDER
# ==============================

def ensure_data_folder():
    os.makedirs(DATA_FOLDER, exist_ok=True)

def clear_old_outputs():
    open(STORYBOARD_FILE, "w").close()
    open(NARRATION_FILE, "w").close()
    open(VISUAL_FILE, "w").close()
    open(SCENES_JSON_FILE, "w").close()
    print("✅ Old outputs cleared")

# ==============================
# LOAD MODEL
# ==============================

def load_llm():
    print("Loading Ollama model...")
    return OllamaLLM(model=OLLAMA_MODEL)

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

    return content

# ==============================
# GENERATE CINEMATIC STORYBOARD
# ==============================

def generate_storyboard(project_text, llm):

    print("Generating EXACTLY 15-scene CINEMATIC storyboard...")

    prompt = f"""
You are a professional cinematic storyboard creator and visual film director.

Generate EXACTLY 15 scenes in VALID JSON.

STRICT RULES:
- Output ONLY JSON array
- No explanation
- No markdown
- Exactly 15 items
- Each item must contain:
    scene_number
    scene_title
    narration_prompt
    visual_prompt

NARRATION RULES:
- 3–4 emotionally engaging and technically clear sentences
- Story-driven and immersive
- Specific to the project

VISUAL RULES (VERY IMPORTANT):
- Minimum 150 words per visual_prompt
- Must be cinematic and realistic
- Use artistic wording
- Include:
    • camera angle (wide shot, close-up, aerial shot, over-the-shoulder, tracking shot, etc.)
    • lighting style (golden hour, neon glow, rim light, soft diffused light, dramatic shadows)
    • depth of field
    • lens type (35mm, 50mm, cinematic lens)
    • realistic environment details
    • textures and materials
    • atmosphere (fog, dust particles, reflections, light rays)
    • emotional mood
- Must look like a professional movie frame or high-end photography
- Ultra realistic
- 4K resolution description
- Cinematic composition

FORMAT:

[
  {{
    "scene_number": 1,
    "scene_title": "",
    "narration_prompt": "",
    "visual_prompt": ""
  }}
]

Project Content:
{project_text}
"""

    response = llm.invoke(prompt)
    return response.strip()

# ==============================
# EXTRACT JSON SAFELY
# ==============================

def extract_json(text):
    match = re.search(r"\[\s*{.*}\s*\]", text, re.DOTALL)
    if match:
        return match.group(0)
    return None

# ==============================
# SAVE OUTPUTS
# ==============================

def save_outputs(raw_text):

    json_text = extract_json(raw_text)

    if not json_text:
        print("❌ Could not extract JSON from model output.")
        with open(STORYBOARD_FILE, "w", encoding="utf-8") as f:
            f.write(raw_text)
        return

    try:
        scenes = json.loads(json_text)

        if len(scenes) != 15:
            print(f"⚠ Warning: Model returned {len(scenes)} scenes instead of 15")

        # Save formatted storyboard
        with open(STORYBOARD_FILE, "w", encoding="utf-8") as f:
            for scene in scenes:
                f.write(f"Scene {scene['scene_number']}: {scene['scene_title']}\n\n")
                f.write("Narration:\n")
                f.write(scene["narration_prompt"] + "\n\n")
                f.write("Visual:\n")
                f.write(scene["visual_prompt"] + "\n\n")
                f.write("=" * 80 + "\n\n")

        # Save narration only
        with open(NARRATION_FILE, "w", encoding="utf-8") as narr:
            for scene in scenes:
                narr.write(
                    f"Scene {scene['scene_number']}: "
                    f"{scene['narration_prompt']}\n\n"
                )

        # Save visual prompts only
        with open(VISUAL_FILE, "w", encoding="utf-8") as visual:
            for scene in scenes:
                visual.write(
                    f"Scene {scene['scene_number']}:\n"
                    f"{scene['visual_prompt']}\n\n"
                )

        # Save structured JSON
        with open(SCENES_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(scenes, f, indent=4)

        print("✅ storyboard.txt saved")
        print("✅ narration.txt saved")
        print("✅ visual_prompts.txt saved")
        print("✅ scenes.json saved")

    except Exception as e:
        print("❌ JSON parsing failed.")
        print("Error:", e)

        with open(STORYBOARD_FILE, "w", encoding="utf-8") as f:
            f.write(raw_text)

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("\n===== STORYBOARD GENERATOR (CINEMATIC REALISM VERSION) =====\n")

    ensure_data_folder()
    clear_old_outputs()

    project_text = read_rag_output()
    if not project_text:
        exit()

    llm = load_llm()

    raw_output = generate_storyboard(project_text, llm)

    save_outputs(raw_output)

    print("\n🎬 Cinematic storyboard generation complete!")