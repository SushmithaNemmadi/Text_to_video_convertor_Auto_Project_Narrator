import os
import re
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw, ImageFont

print("Loading Animated Model (CPU mode)...")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
)

pipe = pipe.to("cpu")


# ---------------------------
# Extract Visual Prompts
# ---------------------------
def extract_visual_prompts(storyboard_text):
    visuals = re.findall(r"Visual:\s*(.+)", storyboard_text)
    return visuals


# ---------------------------
# Enhance Prompt
# ---------------------------
def enhance_prompt(prompt):
    return f"""
    2D animated illustration,
    clean flat design,
    explainer video style,
    smooth shading,
    professional presentation slide,
    no text, no letters, no typography,
    {prompt}
    """


# ---------------------------
# Generate Image
# ---------------------------
def generate_image(prompt, filename):
    print(f"Generating image: {filename}")

    image = pipe(
        enhance_prompt(prompt),
        height=512,
        width=512,
        num_inference_steps=25
    ).images[0]

    image.save(filename)


# ---------------------------
# Add Clean English Text
# ---------------------------
def add_clean_text(image_path, scene_number, caption_text):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_caption = ImageFont.truetype("arial.ttf", 28)
    except:
        font_title = ImageFont.load_default()
        font_caption = ImageFont.load_default()

    width, height = image.size

    # Draw white background box at top
    draw.rectangle([(0, 0), (width, 90)], fill="white")

    # Scene Title
    title = f"Scene {scene_number}"
    draw.text((20, 20), title, fill="black", font=font_title)

    # Caption (short)
    draw.text((20, 60), caption_text, fill="black", font=font_caption)

    image.save(image_path)


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":

    os.makedirs("images", exist_ok=True)

    storyboard_path = "data/storyboard.txt"

    if not os.path.exists(storyboard_path):
        print("ERROR: storyboard.txt not found.")
        exit()

    with open(storyboard_path, "r", encoding="utf-8") as f:
        storyboard = f.read()

    visuals = extract_visual_prompts(storyboard)
    narrations = re.findall(r"Narration:\s*(.+)", storyboard)

    print(f"Found {len(visuals)} scenes. Generating images...\n")

    for i, prompt in enumerate(visuals, start=1):
        filename = f"images/scene{i}.png"

        generate_image(prompt, filename)

        caption = narrations[i-1] if i-1 < len(narrations) else ""
        add_clean_text(filename, i, caption)

    print("\n✅ All images generated successfully!")
