const API = "http://localhost:5000";

document
.getElementById("projectForm")
.addEventListener("submit", async function(e){

    e.preventDefault();

    const title =
    document.getElementById("projectTitle").value;

    const description =
    document.getElementById("projectDescription").value;

    if(!title && !description){
        alert("Enter project title or description");
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
            alert("Error starting generation");
            return;
        }

        // Save job ID for progress tracking
        localStorage.setItem("job_id", data.job_id);

        // Go to processing page
        window.location.href = "processing.html";

    }
    catch(error){

        console.error("Error:", error);
        alert("Backend connection failed");

    }

});