from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import uuid
import threading
import subprocess
import os

app = Flask(__name__)
CORS(app)

jobs = {}
lock = threading.Lock()

BASE_DIR = os.getcwd()
OUTPUT_VIDEO = os.path.join(BASE_DIR, "final_video.mp4")
OUTPUT_DOC = os.path.join(BASE_DIR, "project_documentation.docx")


# -------------------------------
# GENERATE JOB
# -------------------------------

@app.route("/api/generate", methods=["POST"])
def generate():

    data = request.get_json()

    title = data.get("project_topic", "")
    description = data.get("project_description", "")

    if not title and not description:
        return jsonify({"error": "Enter title or description"}), 400

    query = f"{title} {description}".strip()

    job_id = str(uuid.uuid4())

    with lock:
        jobs[job_id] = {
            "id": job_id,
            "status": "Starting generation...",
            "progress": 5,
            "video": None,
            "doc": None
        }

    thread = threading.Thread(target=run_job, args=(job_id, query), daemon=True)
    thread.start()

    return jsonify({"job_id": job_id})


# -------------------------------
# RUN PIPELINE
# -------------------------------

def run_job(job_id, query):

    process = subprocess.Popen(
        ["python", "-u", "backend/run_pipeline.py", query],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:

        line = line.strip()
        print("PIPELINE:", line, flush=True)

        if "STAGE: RAG_START" in line:
            update_job(job_id, "Generating project documentation...", 10)

        elif "STAGE: STORYBOARD" in line:
            update_job(job_id, "Creating storyboard...", 30)

        elif "STAGE: IMAGES" in line:
            update_job(job_id, "Generating images...", 50)

        elif "STAGE: AUDIO" in line:
            update_job(job_id, "Generating narration audio...", 70)

        elif "STAGE: DIAGRAM" in line:
            update_job(job_id, "Generating diagrams...", 80)

        elif "STAGE: VIDEO" in line:
            update_job(job_id, "Rendering final video...", 90)

        elif "STAGE: COMPLETE" in line:

            with lock:
                jobs[job_id]["video"] = f"/api/video/{job_id}"
                jobs[job_id]["doc"] = f"/api/document/{job_id}"

            update_job(job_id, "Completed", 100)

    process.wait()


# -------------------------------
# UPDATE JOB
# -------------------------------

def update_job(job_id, status, progress):

    with lock:

        if job_id not in jobs:
            return

        current = jobs[job_id]["progress"]

        if progress < current:
            progress = current

        jobs[job_id]["status"] = status
        jobs[job_id]["progress"] = progress


# -------------------------------
# STATUS API
# -------------------------------

@app.route("/api/status/<job_id>")
def status(job_id):

    with lock:
        job = jobs.get(job_id)

    if job is None:
        return jsonify({
            "status": "Initializing...",
            "progress": 0,
            "video": None,
            "doc": None
        })

    return jsonify({
        "status": job["status"],
        "progress": job["progress"],
        "video": job["video"],
        "doc": job["doc"]
    })


# -------------------------------
# VIDEO API
# -------------------------------

@app.route("/api/video/<job_id>")
def video(job_id):

    if not os.path.exists(OUTPUT_VIDEO):
        return jsonify({"error": "Video not ready"}), 404

    return send_file(OUTPUT_VIDEO, mimetype="video/mp4")


# -------------------------------
# DOCUMENT API
# -------------------------------

@app.route("/api/document/<job_id>")
def document(job_id):

    if not os.path.exists(OUTPUT_DOC):
        return jsonify({"error": "Document not ready"}), 404

    return send_file(OUTPUT_DOC, as_attachment=True)


# -------------------------------
# RUN SERVER
# -------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        threaded=True
    )