const API = "http://localhost:5000";

let currentJob = null;
let lastProgress = 0;

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("projectForm");

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        const topic = document.getElementById("projectTitle").value;
        const description = document.getElementById("projectDescription").value;

        if (!topic && !description) {
            alert("Enter title or description");
            return;
        }

        document.getElementById("status").innerText = "🚀 Starting generation...";

        const bar = document.getElementById("progressBar");
        bar.style.width = "5%";

        lastProgress = 5;

        const response = await fetch(API + "/api/generate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                project_topic: topic,
                project_description: description
            })
        });

        const data = await response.json();
        currentJob = data.job_id;

        checkStatus(currentJob);

    });

});


async function checkStatus(jobId) {

    const response = await fetch(API + "/api/status/" + jobId);
    const data = await response.json();

    const progress = parseInt(data.progress);
    const bar = document.getElementById("progressBar");

    if (progress < lastProgress) {
        setTimeout(() => checkStatus(jobId), 2000);
        return;
    }

    lastProgress = progress;

    document.getElementById("status").innerText =
        data.status + " (" + progress + "%)";

    bar.style.width = progress + "%";

    if (progress < 100) {

        setTimeout(() => checkStatus(jobId), 2000);

    } else {

        document.getElementById("status").innerText = "✅ Video Ready";

        if (data.video) {

            const videoPlayer = document.getElementById("videoPlayer");

            videoPlayer.src = API + data.video;
            videoPlayer.load();
            videoPlayer.style.display = "block";

            document.getElementById("downloadVideo").href =
                API + data.video;
        }

        if (data.doc) {

            document.getElementById("downloadDoc").href =
                API + data.doc;
        }
    }
}