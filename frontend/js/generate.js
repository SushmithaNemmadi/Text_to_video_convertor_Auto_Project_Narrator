const API = "http://localhost:5000";

document
.getElementById("projectForm")
.addEventListener("submit", async function(e){


e.preventDefault();

const title =
document.getElementById("projectTitle").value.trim();

const description =
document.getElementById("projectDescription").value.trim();

// ---------------------------
// FRONTEND VALIDATION
// ---------------------------

if(title.length < 5 && description.length < 10){

    alert("Please enter a clear project title or description.\nExample: Smart Parking System using IoT");

    return;

}

try{

    const response = await fetch(API + "/api/generate", {

        method: "POST",

        headers:{
            "Content-Type":"application/json"
        },

        body: JSON.stringify({
            project_topic: title,
            project_description: description
        })

    });

    const data = await response.json();

    if(!data.job_id){

        alert("Failed to start generation.");
        return;

    }

    // Save job id
    localStorage.setItem("job_id", data.job_id);

    // Move to processing page
    window.location.href = "processing.html";

}
catch(error){

    console.error("Backend error:", error);

    alert("Cannot connect to backend server.");

}


});
