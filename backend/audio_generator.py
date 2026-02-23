import os
import re
from gtts import gTTS

print("=== Audio Generator (Colab Version) ===")

os.makedirs("audio", exist_ok=True)

path = "data/narration.txt"

if not os.path.exists(path):
    print("narration.txt not found")
    exit()

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

scenes = re.findall(
    r"Scene \d+:\s*(.*?)(?=\nScene|\Z)",
    content,
    re.DOTALL
)

for i, text in enumerate(scenes, start=1):
    filename = f"audio/scene{i}.wav"
    print("Generating", filename)

    tts = gTTS(text)
    tts.save(filename)

print("Audio generated!")