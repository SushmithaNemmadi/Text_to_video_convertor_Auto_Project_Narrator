import os
import sys
import subprocess
import re

# Force immediate stdout flush
sys.stdout.reconfigure(line_buffering=True)


def log(msg):
    print(msg, flush=True)


# ==============================
# QUERY VALIDATION
# ==============================

def is_valid_query(query):

    query = query.strip()

    # Too short
    if len(query) < 10:
        return False

    # Must contain at least 3 words
    words = query.split()
    if len(words) < 3:
        return False

    # Reject random characters
    if not re.search(r"[a-zA-Z]", query):
        return False

    # Reject repeated same characters like "aaaaa"
    if re.fullmatch(r"(.)\1{5,}", query):
        return False

    return True


# ==============================
# RUN PIPELINE STEP
# ==============================

def run_step(stage, message, command):

    # Stage marker used by Flask
    print(f"STAGE: {stage}", flush=True)

    log(message)

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # Stream subprocess output
    while True:

        line = process.stdout.readline()

        if not line:
            break

        line = line.strip()

        if line:
            print(line, flush=True)

    process.wait()

    if process.returncode != 0:
        log(f"ERROR: {stage} FAILED")
        sys.exit(1)


# ==============================
# START PIPELINE
# ==============================

log("\n===================================")
log("PROJECT -> VIDEO PIPELINE STARTED")
log("===================================\n")

query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

# Validate query
if not is_valid_query(query):

    print("STAGE: INVALID_INPUT", flush=True)

    log("\nERROR: Input query is unclear.")
    log("Please enter a clear project topic.")
    log("Example: 'Smart Parking System using IoT'")

    sys.exit(1)


log(f"Project Topic: {query}")

BACKEND = "backend"


# ==============================
# STEP 1 — RAG
# ==============================

run_step(
    "RAG_START",
    "Generating RAG output...",
    f'python -u {BACKEND}/rag_system.py "{query}"'
)


# ==============================
# STEP 2 — STORYBOARD
# ==============================

run_step(
    "STORYBOARD",
    "Generating storyboard...",
    f"python -u {BACKEND}/generate_storyboard.py"
)


# ==============================
# STEP 3 — IMAGES
# ==============================

run_step(
    "IMAGES",
    "Generating images...",
    f"python -u {BACKEND}/image_generator.py"
)


# ==============================
# STEP 4 — AUDIO
# ==============================

run_step(
    "AUDIO",
    "Generating audio...",
    f"python -u {BACKEND}/audio_generator.py"
)


# ==============================
# STEP 5 — DIAGRAM
# ==============================

run_step(
    "DIAGRAM",
    "Generating diagrams...",
    f"python -u {BACKEND}/diagram_generator.py"
)


# ==============================
# STEP 6 — VIDEO
# ==============================

run_step(
    "VIDEO",
    "Generating video...",
    f"python -u {BACKEND}/video_generator.py"
)


print("STAGE: COMPLETE", flush=True)

log("\n===================================")
log("VIDEO GENERATED SUCCESSFULLY")
log("===================================\n")