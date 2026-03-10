from PIL import Image, ImageDraw, ImageFont
import os

# Folder where images are stored
IMAGE_FOLDER = "images"

# Output folder for labeled images
OUTPUT_FOLDER = "images_with_text"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Example captions for each scene
captions = [
    "AI Resume Analyzer System",
    "User Uploads Resume",
    "AI Model Processes Resume",
    "Resume Data Analysis",
    "Keyword Matching with Job Description",
    "Skill Gap Detection",
    "Feedback Generation",
    "User Reviews Suggestions",
    "Resume Editing",
    "Improved Resume",
    "System Architecture",
    "Backend Processing",
    "Database Storage",
    "User Interface Display",
    "Project Benefits"
]

# Load font
font = ImageFont.truetype("arial.ttf", 40)

# Process each image
for i, file in enumerate(sorted(os.listdir(IMAGE_FOLDER))):

    if file.endswith(".png") or file.endswith(".jpg"):

        path = os.path.join(IMAGE_FOLDER, file)

        img = Image.open(path)

        draw = ImageDraw.Draw(img)

        text = captions[i] if i < len(captions) else "AI System"

        # Position text
        width, height = img.size
        text_position = (50, height - 80)

        # Draw text
        draw.text(text_position, text, fill="white", font=font)

        output_path = os.path.join(OUTPUT_FOLDER, file)

        img.save(output_path)

        print("Saved labeled image:", output_path)

print(" All images updated with readable text")