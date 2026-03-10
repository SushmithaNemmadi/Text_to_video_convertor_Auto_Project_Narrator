const API = "http://localhost:5000";

let currentJob = null;
let progressTimer = null;

/* ==========================
GENERATE VIDEO
========================== */

async function generateVideo() {

    const topic = document.getElementById("topic").value
    const description = document.getElementById("description").value

    if (!topic && !description) {
        alert("Please enter project topic or description")
        return
    }

    document.getElementById("status").innerText = "🚀 Starting generation..."

    const response = await fetch(API + "/api/generate", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            project_topic: topic,
            project_description: description
        })

    })

    const data = await response.json()

    currentJob = data.job_id

    checkStatus(currentJob)

}


/* ==========================
CHECK STATUS
========================== */

async function checkStatus(jobId) {

    const response = await fetch(API + "/api/status/" + jobId)

    const data = await response.json()

    document.getElementById("status").innerText =
        "Status: " + data.status + " (" + data.progress + "%)"

    if (data.status != "completed") {

        progressTimer = setTimeout(() => checkStatus(jobId), 2000)

    }

    else {

        document.getElementById("status").innerText = "✅ Video Ready"

        const videoUrl = API + "/api/video/" + jobId

        const videoPlayer = document.getElementById("videoPlayer")

        videoPlayer.src = videoUrl

        videoPlayer.load()

        const docUrl = API + "/api/document/" + jobId

        document.getElementById("downloadDoc").href = docUrl

        showNotification("Video generated successfully!", "success")
    }

}


/* ==========================
VIDEO PLAYER CONTROLS
========================== */

function togglePlay() {

    const video = document.getElementById("videoPlayer")

    if (video.paused) {
        video.play()
    } else {
        video.pause()
    }

}

function changeVolume(value) {

    const video = document.getElementById("videoPlayer")

    video.volume = value / 100

}

function seekVideo(value) {

    const video = document.getElementById("videoPlayer")

    if (!video.duration) return

    const seekTime = (value / 100) * video.duration

    video.currentTime = seekTime

}

function toggleFullscreen() {

    const video = document.getElementById("videoPlayer")

    if (!document.fullscreenElement) {
        video.requestFullscreen()
    } else {
        document.exitFullscreen()
    }

}


/* ==========================
NOTIFICATION SYSTEM
========================== */

function showNotification(message, type = "info") {

    let container = document.getElementById("notificationContainer")

    if (!container) return

    const div = document.createElement("div")

    div.style.background = "#333"
    div.style.color = "white"
    div.style.padding = "12px"
    div.style.margin = "10px"
    div.style.borderRadius = "6px"

    div.innerText = message

    container.appendChild(div)

    setTimeout(() => {
        div.remove()
    }, 4000)

}


/* ==========================
DOWNLOAD VIDEO
========================== */

function downloadVideo() {

    if (!currentJob) return

    window.open(API + "/api/video/" + currentJob)

}


/* ==========================
RESET FORM
========================== */

function resetForm() {

    document.getElementById("topic").value = ""
    document.getElementById("description").value = ""

    document.getElementById("videoPlayer").src = ""

    document.getElementById("status").innerText = ""

}


/* ==========================
CANCEL GENERATION
========================== */

function cancelGeneration() {

    if (progressTimer) {
        clearTimeout(progressTimer)
    }

    document.getElementById("status").innerText = "❌ Generation cancelled"

}