import os
import re
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

print("=== Video Generator ===")

images_folder = "images"
audio_folder = "audio"
output_video = "final_video.mp4"


def extract_number(filename):
    nums = re.findall(r"\d+", filename)
    return int(nums[0]) if nums else 0


image_files = sorted(
    [f for f in os.listdir(images_folder) if f.endswith(".png")],
    key=extract_number
)

audio_files = sorted(
    [f for f in os.listdir(audio_folder) if f.endswith(".wav")],
    key=extract_number
)

if len(image_files) != len(audio_files):
    print("❌ Image/audio count mismatch")
    exit()

clips = []

for img, aud in zip(image_files, audio_files):
    print(f"Combining {img} + {aud}")

    audio_clip = AudioFileClip(os.path.join(audio_folder, aud))
    image_clip = ImageClip(os.path.join(images_folder, img)).set_duration(audio_clip.duration)

    image_clip = image_clip.set_audio(audio_clip)
    clips.append(image_clip)

print("Rendering final video...")

final_video = concatenate_videoclips(clips)
final_video.write_videofile(output_video, fps=24)

print("✅ Video generated!")