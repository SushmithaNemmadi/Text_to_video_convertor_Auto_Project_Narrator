const API = "http://localhost:5000";

const jobId = localStorage.getItem("job_id");

if(!jobId){

    alert("No job found");
    window.location.href = "generate.html";

}

async function checkStatus(){

    try{

        const response = await fetch(API + "/api/status/" + jobId);
        const data = await response.json();

        // Update progress bar
        const bar = document.getElementById("progressBar");
        bar.style.width = data.progress + "%";

        // Update status text
        const statusText = document.getElementById("statusText");
        if(statusText){
            statusText.innerText = data.status;
        }

        // If generation completed
        if(data.progress >= 100){

            localStorage.setItem("video_url", API + data.video);
            localStorage.setItem("doc_url", API + data.doc);

            window.location.href = "result.html";
            return;
        }

        // If invalid input detected
        if(data.status.includes("Invalid")){

            alert(data.status);
            window.location.href = "generate.html";
            return;

        }

        // Continue polling
        setTimeout(checkStatus, 2000);

    }
    catch(err){

        console.error("Status error:", err);
        setTimeout(checkStatus, 3000);

    }

}

checkStatus();