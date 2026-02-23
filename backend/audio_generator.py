import os
import re
import pyttsx3

print("=== Scene-wise Audio Generator ===")

os.makedirs("audio", exist_ok=True)

narration_path = "data/narration.txt"

if not os.path.exists(narration_path):
    print("❌ narration.txt not found!")
    exit()

with open(narration_path, "r", encoding="utf-8") as f:
    content = f.read()

# multi-line scene extraction
scenes = re.findall(
    r"Scene \d+:\s*(.*?)(?=\nScene|\Z)",
    content,
    re.DOTALL
)

if not scenes:
    print("❌ No scenes found in narration.txt")
    exit()

engine = pyttsx3.init()
engine.setProperty("rate", 170)

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

for i, text in enumerate(scenes, start=1):
    filename = f"audio/scene{i}.wav"
    print(f"Generating {filename}")
    engine.save_to_file(text.strip(), filename)

engine.runAndWait()

print("✅ All audio generated!")