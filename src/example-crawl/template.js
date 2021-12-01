var my_width = 0
var requestId = 0
var my_pixels = 0
var my_pixel = 2 //speed of animation

function escapeHtml(unsafe) {
    return unsafe.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;").replace(/  /g, "&nbsp;").replace(/\n/g, "<br>")
}

function init() {
    my_width = document.getElementById('main').clientWidth + 1
    document.getElementById('main').style.left = ( window.innerWidth - 100 )+ "px"
    document.getElementById('main').style.visibility = "visible"
}


function animate() {
    document.getElementById("main").style.left = ((window.innerWidth) - my_pixels) + "px"
    my_pixels = my_pixels + my_pixel
    if ((my_width + window.innerWidth) <= my_pixels) {
		console.log("Restarting")
        my_pixels = 0
        document.getElementById("main").style.left = ((window.innerWidth) + 1)  + "px"
        play()
    } else {
        if (stop_me_please != true) {
			requestId = window.requestAnimationFrame(animate)
		}
    }
}

function play() {
    stop_me_please = false;
    requestId = window.requestAnimationFrame(animate);
}

function stop(){
    if (requestId)
        window.cancelAnimationFrame(requestId);
    stop_me_please = true;
    requestId = 0;
}

function update(str){
    var params = parse_params(str)
    if (params["text"])
        document.getElementById("main").innerHTML = escapeHtml(params["text"])
}


document.addEventListener("DOMContentLoaded", function(event) { 
	init()
	play()
})
