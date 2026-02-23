import subprocess
import sys
import os

print("🚀 ===== AI PROJECT VIDEO GENERATION PIPELINE =====")

SCRIPTS = [
    "rag_system.py",
    "generate_storyboard.py",
    "audio_generator.py",
    "image_generator.py",
    "video_generator.py"
]


def run_script(script_name):
    print(f"\n▶ Running {script_name}...\n")

    script_path = os.path.join("backend", script_name)

    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        exit()

    result = subprocess.run([sys.executable, script_path])

    if result.returncode != 0:
        print(f"❌ Error running {script_name}")
        exit()

    print(f"✅ {script_name} completed")


if __name__ == "__main__":

    for script in SCRIPTS:
        run_script(script)

    print("\n🎉 VIDEO GENERATED SUCCESSFULLY!")