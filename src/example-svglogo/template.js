// Create a timeline and start in a paused state
var timeline = gsap.timeline();
timeline.pause();

// We add spin-in effect to the logo
timeline.from("#logo",  {duration: .6, opacity:0, rotationY: "-90"});

//
// CasparCG handlers
//

function play(){
    // show the #container, which is hidden by default and start the animation
    document.getElementById("container").setAttribute("class", "visible");
    timeline.play();
}

function stop(){
    // to hide the layout, just play the timeline in reverse
    timeline.reverse();
}

function update(data){
    var params = parse_params(data);
    console.log("UPDATE",params)
    if ("Position" in params)
        document.getElementById("logo").setAttribute("class", params["Position"])
}
