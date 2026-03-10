const API = "http://localhost:5000";

let currentJob = null;


/* GENERATE VIDEO */

document.getElementById("projectForm").addEventListener("submit", async function(e){

    e.preventDefault();

    const topic = document.getElementById("projectTitle").value
    const description = document.getElementById("projectDescription").value

    if(!topic && !description){
        alert("Enter title or description")
        return
    }

    document.getElementById("status").innerText =
    "🚀 Starting generation..."

    const response = await fetch(API + "/api/generate",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            project_topic:topic,
            project_description:description
        })

    })

    const data = await response.json()

    currentJob = data.job_id

    checkStatus(currentJob)

})


/* CHECK STATUS */

async function checkStatus(jobId){

    const response = await fetch(API + "/api/status/"+jobId)

    const data = await response.json()

    document.getElementById("status").innerText =
    data.status + " (" + data.progress + "%)"

    if(data.progress < 100){

        setTimeout(()=>checkStatus(jobId),2000)

    }

    else{

        document.getElementById("status").innerText =
        "✅ Video Ready"

        const videoUrl = API + "/api/video/"+jobId

        document.getElementById("videoPlayer").src = videoUrl

        document.getElementById("downloadVideo").href = videoUrl

        const docUrl = API + "/api/document/"+jobId

        document.getElementById("downloadDoc").href = docUrl

    }

}