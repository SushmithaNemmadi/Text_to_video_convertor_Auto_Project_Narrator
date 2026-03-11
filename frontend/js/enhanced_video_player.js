const videoPlayer = document.getElementById("videoPlayer");
const statusText = document.getElementById("status");

if(videoPlayer){

    // When video starts loading
    videoPlayer.addEventListener("loadstart", function(){

        console.log("Video loading...");
        if(statusText){
            statusText.innerText = "🎬 Loading generated video...";
        }

    });

    // When video metadata is ready
    videoPlayer.addEventListener("loadedmetadata", function(){

        console.log("Video metadata loaded");

    });

    // When video can start playing
    videoPlayer.addEventListener("canplay", function(){

        console.log("Video ready to play");

        if(statusText){
            statusText.innerText = "✅ Video Ready";
        }

    });

    // If video fails
    videoPlayer.addEventListener("error", function(){

        console.error("Video failed to load");

        if(statusText){
            statusText.innerText = "❌ Failed to load video";
        }

    });

    // Optional: autoplay when video appears
    videoPlayer.addEventListener("loadeddata", function(){

        setTimeout(() => {

            videoPlayer.play().catch(() => {
                console.log("Autoplay blocked by browser");
            });

        }, 500);

    });

}