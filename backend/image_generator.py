import os
import re
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw, ImageFont

print("Loading Stable Diffusion (CPU mode)...")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
)

pipe = pipe.to("cpu")
pipe.enable_attention_slicing()  # faster CPU


def extract_visuals(text):
    return re.findall(
        r"Visual:\s*(.*?)(?=\nScene|\Z)",
        text,
        re.DOTALL
    )


def extract_narrations(text):
    return re.findall(
        r"Narration:\s*(.*?)(?=\nVisual:)",
        text,
        re.DOTALL
    )


def enhance_prompt(prompt):
    return f"""
    2D animated illustration,
    clean flat design,
    explainer video style,
    no text,
    {prompt}
    """


def add_text(image_path, scene_number, caption):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()

    draw.rectangle([(0, 0), (512, 80)], fill="white")
    draw.text((10, 10), f"Scene {scene_number}", fill="black", font=font)
    draw.text((10, 40), caption[:80], fill="black", font=font)

    image.save(image_path)


if __name__ == "__main__":

    os.makedirs("images", exist_ok=True)

    path = "data/storyboard.txt"

    if not os.path.exists(path):
        print("❌ storyboard.txt not found")
        exit()

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    visuals = extract_visuals(text)
    narrations = extract_narrations(text)

    if len(visuals) == 0:
        print("❌ No visual prompts found")
        exit()

    print(f"Generating {len(visuals)} images...\n")

    for i, prompt in enumerate(visuals, start=1):
        image = pipe(enhance_prompt(prompt), num_inference_steps=20).images[0]
        filename = f"images/scene{i}.png"
        image.save(filename)

        caption = narrations[i-1] if i-1 < len(narrations) else ""
        add_text(filename, i, caption)

    print("✅ Images generated!")