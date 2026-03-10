import os
import asyncio
import edge_tts

print("=== Audio Generator (Edge TTS Version) ===")

data_file = "data/narration.txt"
audio_folder = "audio"

VOICE = "en-IN-PrabhatNeural"

os.makedirs(audio_folder, exist_ok=True)


# Delete old audio
for file in os.listdir(audio_folder):
    if file.endswith(".mp3") or file.endswith(".wav"):
        os.remove(os.path.join(audio_folder, file))


# Read narration
with open(data_file, "r", encoding="utf-8") as f:
    lines = f.readlines()


# Split scenes
scenes = []
current = ""

for line in lines:

    line = line.strip()

    if line.lower().startswith("scene"):

        if current != "":
            scenes.append(current.strip())
            current = ""

    else:
        current += " " + line

if current != "":
    scenes.append(current.strip())


print("Scenes:", len(scenes))


# Generate audio using Edge TTS
async def generate_audio():

    for i, text in enumerate(scenes):

        filename = f"audio/{i}.mp3"

        print("Creating", filename)

        communicate = edge_tts.Communicate(
            text,
            VOICE,
            rate="-10%",
            pitch="+0Hz"
        )

        await communicate.save(filename)

    print("All Audio Generated")


asyncio.run(generate_audio())