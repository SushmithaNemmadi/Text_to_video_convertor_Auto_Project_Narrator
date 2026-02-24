import os
import re
import pyttsx3

print("=== ProjVision Part 3: Scene-wise Audio Generator ===")

os.makedirs("audio", exist_ok=True)

# Load narration file
narration_path = "data/narration.txt"

if not os.path.exists(narration_path):
    print("narration.txt not found!")
    exit()

with open(narration_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract scene narrations
scenes = re.findall(r"Scene \d+:\s*(.+)", content)

engine = pyttsx3.init()
engine.setProperty('rate', 170)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

for i, text in enumerate(scenes, start=1):
    filename = f"audio/scene{i}.mp3"
    print(f"Generating {filename}")
    engine.save_to_file(text, filename)

engine.runAndWait()

print("\n✅ All scene audios generated successfully!")
