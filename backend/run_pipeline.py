import os
import sys

print("\n===================================")
print("PROJECT -> VIDEO PIPELINE STARTED")
print("===================================\n")

# ==============================
# STEP 1 — GET QUERY
# ==============================

query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Default Project"

print("Project Topic:", query)

BACKEND = "backend"

# ==============================
# STEP 2 — RAG SYSTEM
# ==============================

print("STAGE: RAG_START")
print("Generating RAG output...")

os.system(f'python {BACKEND}/rag_system.py "{query}"')


# ==============================
# STEP 3 — STORYBOARD
# ==============================

print("STAGE: STORYBOARD")
print("Generating storyboard...")

os.system(f"python {BACKEND}/generate_storyboard.py")


# ==============================
# STEP 4 — IMAGES
# ==============================

print("STAGE: IMAGES")
print("Generating images...")

os.system(f"python {BACKEND}/image_generator.py")


# ==============================
# STEP 5 — AUDIO
# ==============================

print("STAGE: AUDIO")
print("Generating audio...")

os.system(f"python {BACKEND}/audio_generator.py")


# ==============================
# STEP 6 — VIDEO
# ==============================

print("STAGE: VIDEO")
print("Generating video...")

os.system(f"python {BACKEND}/video_generator.py")


# ==============================
# FINISH
# ==============================

print("STAGE: COMPLETE")

print("\n===================================")
print("VIDEO GENERATED SUCCESSFULLY")
print("Output: backend/final_video.mp4")
print("===================================\n")