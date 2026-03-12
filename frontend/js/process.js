let progress = 0;

let interval = setInterval(()=>{

progress += 10;

document
.getElementById("progressBar")
.style.width = progress + "%";

if(progress >= 100){

clearInterval(interval);

window.location.href = "result.html";

}

},700);