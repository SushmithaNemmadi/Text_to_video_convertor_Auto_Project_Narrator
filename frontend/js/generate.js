document
.getElementById("projectForm")
.addEventListener("submit", function(e){

e.preventDefault();

const title =
document.getElementById("projectTitle").value;

const description =
document.getElementById("projectDescription").value;

localStorage.setItem("title", title);
localStorage.setItem("description", description);

window.location.href = "processing.html";

});