import os

# Force FFmpeg
os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

from moviepy.editor import *

print("=== Testing Audio Merge FINAL ===")

# Convert MP3 → WAV automatically
audio_original = AudioFileClip("audio/0.mp3")

audio_original.write_audiofile("temp.wav")

audio = AudioFileClip("temp.wav")

print("Audio Duration:", audio.duration)


video = ColorClip((640,480), color=(0,0,0))

video = video.set_duration(audio.duration)

video = video.set_audio(audio)


print("\nRendering video...")

video.write_videofile(
    "test_output.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)

print("\n✅ Finished")