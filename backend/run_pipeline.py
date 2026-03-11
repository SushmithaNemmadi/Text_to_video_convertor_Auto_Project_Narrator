import os
import sys
import subprocess

# Force immediate stdout flush
sys.stdout.reconfigure(line_buffering=True)


def log(msg):
    print(msg, flush=True)


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


log("\n===================================")
log("PROJECT -> VIDEO PIPELINE STARTED")
log("===================================\n")

query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Default Project"

log(f"Project Topic: {query}")

BACKEND = "backend"


# STEP 1 — RAG
run_step(
    "RAG_START",
    "Generating RAG output...",
    f'python -u {BACKEND}/rag_system.py "{query}"'
)


# STEP 2 — STORYBOARD
run_step(
    "STORYBOARD",
    "Generating storyboard...",
    f"python -u {BACKEND}/generate_storyboard.py"
)


# STEP 3 — IMAGES
run_step(
    "IMAGES",
    "Generating images...",
    f"python -u {BACKEND}/image_generator.py"
)


# STEP 4 — AUDIO
run_step(
    "AUDIO",
    "Generating audio...",
    f"python -u {BACKEND}/audio_generator.py"
)


# STEP 5 — VIDEO
run_step(
    "VIDEO",
    "Generating video...",
    f"python -u {BACKEND}/video_generator.py"
)


print("STAGE: COMPLETE", flush=True)

log("\n===================================")
log("VIDEO GENERATED SUCCESSFULLY")
log("===================================\n")