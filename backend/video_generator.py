import os
import re

# Force new FFmpeg (important)
os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

print("=== ProjVision Video Generator ===")


# =========================
# PATHS
# =========================

images_folder = "images"
audio_folder = "audio"
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
     if f.endswith(".wav") or f.endswith(".mp3")],
    key=extract_number
)


print("Images Found:", len(image_files))
print("Audio Found:", len(audio_files))


# =========================
# ERROR CHECK
# =========================

if len(audio_files) == 0:
    print("\n❌ ERROR: No audio files found")
    exit()

if len(image_files) != len(audio_files):
    print("\n⚠ Warning: Count mismatch")
    print("Using minimum count\n")


# =========================
# CREATE CLIPS
# =========================

clips = []

for img, aud in zip(image_files, audio_files):

    print("Combining:", img, "+", aud)

    image_path = os.path.join(images_folder, img)
    audio_path = os.path.join(audio_folder, aud)

    audio_clip = AudioFileClip(audio_path)

    print("Audio Duration:", audio_clip.duration)

    image_clip = ImageClip(image_path)

    image_clip = image_clip.set_duration(audio_clip.duration)

    image_clip = image_clip.set_audio(audio_clip)

    image_clip = image_clip.resize((1280,720))

    clips.append(image_clip)


# =========================
# MERGE VIDEO
# =========================

print("\nMerging clips...")

final_video = concatenate_videoclips(clips, method="compose")


# =========================
# EXPORT VIDEO (VS CODE AUDIO FIX)
# =========================

print("\nRendering video with audio...")

final_video.write_videofile(
    output_video,
    fps=24,
    codec="libx264",

    # MP3 audio works inside VS Code
    audio_codec="libmp3lame",

    audio_bitrate="192k",

    temp_audiofile="temp_audio.mp3",
    remove_temp=True
)


print("\n✅ SUCCESS!")
print("Video saved as:", output_video)
print("🔊 Audio works inside VS Code and Media Players")