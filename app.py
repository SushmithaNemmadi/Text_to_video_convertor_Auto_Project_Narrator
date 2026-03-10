from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import uuid
import threading
import subprocess
import os

app = Flask(__name__)
CORS(app)

VIDEO_PATH = "final_video.mp4"
DOC_PATH = "project_documentation.docx"

jobs = {}
lock = threading.Lock()


# ==========================
# GENERATE VIDEO
# ==========================

@app.route("/api/generate", methods=["POST"])
def generate():

    data = request.get_json()

    title = data.get("project_topic", "")
    description = data.get("project_description", "")

    if not title and not description:
        return jsonify({"error": "Enter title or description"}), 400

    query = f"{title} {description}"

    job_id = str(uuid.uuid4())

    job_data = {
        "id": job_id,
        "status": "Starting...",
        "progress": 0
    }

    with lock:
        jobs[job_id] = job_data

    thread = threading.Thread(target=run_job, args=(job_id, query))
    thread.start()

    return jsonify({
        "job_id": job_id
    })


# ==========================
# RUN PIPELINE
# ==========================

def run_job(job_id, query):

    process = subprocess.Popen(
        ["python", "backend/run_pipeline.py", query],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:

        line = line.strip()
        print(line)

        if "STAGE: RAG_START" in line:
            update_job(job_id, "Generating RAG output...", 10)

        elif "STAGE: STORYBOARD" in line:
            update_job(job_id, "Generating storyboard...", 30)

        elif "STAGE: IMAGES" in line:
            update_job(job_id, "Generating images...", 50)

        elif "STAGE: AUDIO" in line:
            update_job(job_id, "Generating audio...", 70)

        elif "STAGE: VIDEO" in line:
            update_job(job_id, "Generating video...", 90)

        elif "STAGE: COMPLETE" in line:
            update_job(job_id, "Completed", 100)

    process.wait()


def update_job(job_id, status, progress):

    with lock:
        if job_id in jobs:
            jobs[job_id]["status"] = status
            jobs[job_id]["progress"] = progress


# ==========================
# STATUS
# ==========================

@app.route("/api/status/<job_id>")
def status(job_id):

    job = jobs.get(job_id)

    if not job:
        return jsonify({"error": "Job not found"}), 404

    return jsonify(job)


# ==========================
# VIDEO
# ==========================

@app.route("/api/video/<job_id>")
def video(job_id):

    if not os.path.exists(VIDEO_PATH):
        return jsonify({"error": "Video not found"}), 404

    return send_file(VIDEO_PATH, mimetype="video/mp4")


# ==========================
# DOCUMENT
# ==========================

@app.route("/api/document/<job_id>")
def document(job_id):

    if not os.path.exists(DOC_PATH):
        return jsonify({"error": "Document not found"}), 404

    return send_file(DOC_PATH, as_attachment=True)


# ==========================
# SERVER
# ==========================

if __name__ == "__main__":
    app.run(debug=True)