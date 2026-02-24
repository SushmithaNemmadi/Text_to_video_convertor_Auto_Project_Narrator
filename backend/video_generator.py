import os
import re
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

print("=== ProjVision Part 4: Correct Scene Sync Video Generator ===")

images_folder = "images"
audio_folder = "audio"
output_video = "final_video.mp4"

def extract_number(filename):
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else 0

image_files = sorted(
    [f for f in os.listdir(images_folder) if f.endswith(".png")],
    key=extract_number
)

audio_files = sorted(
    [f for f in os.listdir(audio_folder) if f.endswith(".mp3")],
    key=extract_number
)

if len(image_files) != len(audio_files):
    print("❌ Number of images and audio files do not match!")
    print(f"Images: {len(image_files)}")
    print(f"Audio: {len(audio_files)}")
    exit()

clips = []

for img_file, audio_file in zip(image_files, audio_files):

    image_path = os.path.join(images_folder, img_file)
    audio_path = os.path.join(audio_folder, audio_file)

    print(f"Combining {img_file} with {audio_file}")

    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path).set_duration(audio_clip.duration)

    image_clip = image_clip.set_audio(audio_clip)

    clips.append(image_clip)

print("\nRendering final video...")

final_video = concatenate_videoclips(clips, method="compose")
final_video.write_videofile(output_video, fps=24)

print("\n✅ Video generated successfully with correct scene sync!")
