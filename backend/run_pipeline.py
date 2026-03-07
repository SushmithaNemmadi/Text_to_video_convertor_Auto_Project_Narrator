import os

print("\n===================================")
print("🚀 PROJECT → VIDEO PIPELINE STARTED")
print("===================================\n")


# ==============================
# STEP 1 — USER INPUT
# ==============================

query = input("\nAsk about any project: ")


# Backend folder path
BACKEND = "backend"


# ==============================
# STEP 2 — RUN RAG SYSTEM
# ==============================

print("\n🔎 Running RAG System...\n")

os.system(f'python {BACKEND}/rag_system.py "{query}"')


# ==============================
# STEP 3 — GENERATE STORYBOARD
# ==============================

print("\n🎬 Generating Storyboard...\n")

os.system(f"python {BACKEND}/generate_storyboard.py")


# ==============================
# STEP 4 — GENERATE AUDIO
# ==============================

print("\n🎤 Generating Audio...\n")

os.system(f"python {BACKEND}/audio_generator.py")


# ==============================
# STEP 5 — GENERATE IMAGES
# ==============================

print("\n🖼 Generating Images...\n")

os.system(f"python {BACKEND}/image_generator.py")


# ==============================
# STEP 6 — GENERATE VIDEO
# ==============================

print("\n🎥 Generating Video...\n")

os.system(f"python {BACKEND}/video_generator.py")


# ==============================
# FINISHED
# ==============================

print("\n===================================")
print("✅ VIDEO GENERATED SUCCESSFULLY")
print("📁 Output → backend/final_video.mp4")
print("===================================\n")