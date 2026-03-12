import os
import asyncio
import edge_tts

print("=== Audio Generator (Edge TTS Version) ===")

data_file = "data/narration.txt"
audio_folder = "audio"

VOICE = "en-IN-PrabhatNeural"

os.makedirs(audio_folder, exist_ok=True)


# ==============================
# DELETE OLD AUDIO
# ==============================

for file in os.listdir(audio_folder):
    if file.endswith(".mp3") or file.endswith(".wav"):
        os.remove(os.path.join(audio_folder, file))


# ==============================
# READ NARRATION FILE
# ==============================

with open(data_file, "r", encoding="utf-8") as f:
    lines = f.readlines()


# ==============================
# SPLIT SCENES AND CLEAN TEXT
# ==============================

scenes = []
current = ""

for line in lines:

    line = line.strip()

    # Remove markdown symbols like **
    line = line.replace("**", "").strip()

    # Skip empty lines
    if line == "":
        continue

    # Detect new scene
    if line.lower().startswith("scene"):

        if current != "":
            scenes.append(current.strip())
            current = ""

    else:
        current += " " + line


# add last scene
if current != "":
    scenes.append(current.strip())


print("Scenes:", len(scenes))


# ==============================
# GENERATE AUDIO USING EDGE TTS
# ==============================

async def generate_audio():

    for i, text in enumerate(scenes):

        filename = f"{audio_folder}/{i}.mp3"

        print("Creating", filename)

        communicate = edge_tts.Communicate(
            text,
            VOICE,
            rate="-10%",
            pitch="+0Hz"
        )

        await communicate.save(filename)

    print("All Audio Generated")


# ==============================
# RUN
# ==============================

asyncio.run(generate_audio())