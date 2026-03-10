import os
import re
import numpy as np
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Force FFmpeg
os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips

print("=== ProjVision Video Generator ===")

# =========================
# PATHS
# =========================

images_folder = "images"
audio_folder = "audio"
narration_file = "data/narration.txt"
output_video = "final_video.mp4"

# =========================
# DELETE OLD VIDEO
# =========================

if os.path.exists(output_video):
    os.remove(output_video)
    print("Old video deleted")

# =========================
# SORT FUNCTION
# =========================

def extract_number(filename):
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else 0

# =========================
# LOAD IMAGES
# =========================

image_files = sorted(
    [f for f in os.listdir(images_folder)
     if f.endswith(".png") or f.endswith(".jpg")],
    key=extract_number
)

# =========================
# LOAD AUDIO
# =========================

audio_files = sorted(
    [f for f in os.listdir(audio_folder)
     if f.endswith(".mp3") or f.endswith(".wav")],
    key=extract_number
)

print("Images Found:", len(image_files))
print("Audio Found:", len(audio_files))

# =========================
# LOAD SUBTITLES (IGNORE SCENE TITLES)
# =========================

subtitles = []

if os.path.exists(narration_file):

    with open(narration_file, "r", encoding="utf-8") as f:

        for line in f.readlines():

            line = line.strip()

            if not line:
                continue

            if line.lower().startswith("scene"):
                continue

            subtitles.append(line)

subtitles = subtitles[:len(audio_files)]

print("Subtitles Loaded:", len(subtitles))

# =========================
# FONT (SMALLER FOR CLEAR VISIBILITY)
# =========================

font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)

# =========================
# CREATE SUBTITLE IMAGE
# =========================

def create_subtitle(text):

    width = 1280
    height = 110

    # Wrap long sentences
    text = "\n".join(textwrap.wrap(text, width=60))

    # Light transparent background
    img = Image.new("RGBA", (width, height), (0,0,0,120))
    draw = ImageDraw.Draw(img)

    bbox = draw.multiline_textbbox((0,0), text, font=font)

    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (width - text_w)//2
    y = (height - text_h)//2

    draw.multiline_text(
        (x,y),
        text,
        font=font,
        fill="white",
        stroke_width=1,
        stroke_fill="black",
        align="center"
    )

    return np.array(img)

# =========================
# CREATE VIDEO CLIPS
# =========================

clips = []

for i,(img,aud) in enumerate(zip(image_files,audio_files)):

    print("Combining:", img, "+", aud)

    image_path = os.path.join(images_folder,img)
    audio_path = os.path.join(audio_folder,aud)

    audio_clip = AudioFileClip(audio_path)

    print("Audio Duration:", audio_clip.duration)

    image_clip = ImageClip(image_path)
    image_clip = image_clip.set_duration(audio_clip.duration)
    image_clip = image_clip.resize((1280,720))
    image_clip = image_clip.set_audio(audio_clip)

    text = subtitles[i] if i < len(subtitles) else ""

    subtitle_img = create_subtitle(text)

    subtitle_clip = ImageClip(subtitle_img)
    subtitle_clip = subtitle_clip.set_duration(audio_clip.duration)

    # Position subtitles above video controls
    subtitle_clip = subtitle_clip.set_position(("center", 580))

    final_clip = CompositeVideoClip([image_clip, subtitle_clip])
    final_clip = final_clip.set_audio(audio_clip)

    clips.append(final_clip)

# =========================
# MERGE VIDEO
# =========================

print("\nMerging clips...")

final_video = concatenate_videoclips(clips, method="compose")

# =========================
# EXPORT VIDEO
# =========================

print("\nRendering video with audio...")

final_video.write_videofile(
    output_video,
    fps=24,
    codec="libx264",
    audio_codec="libmp3lame",
    audio_bitrate="192k",
    temp_audiofile="temp_audio.mp3",
    remove_temp=True
)

print("\nSUCCESS!")
print("Video saved as:", output_video)
print("Audio + Subtitles working perfectly")
