// Map parameters (data fields defined in the manifest) to the DOM elements
var data_fields = {
    "MainText"   : "main-text",
    "HeaderText" : "header-text",
    "LowerText"  : "lower-text",
    "Info"       : "info",
    "Label"      : "label"
}

// Create a timeline and start in a paused state
var timeline = gsap.timeline();
timeline.pause();

// first we add a red rectangle spin-in effect
timeline.from("#info",               {duration: .6, opacity:0, rotationY: "-90"});

// main-text animation needs to start slightly before the first animation ends
timeline.from("#main-text",          {duration: .3, opacity:0, x: "-100%"}, "-=0.1");

// as soon the main-text animation finishes, slide down the bottom line
timeline.from("#label, #lower-text", {duration: .3, opacity:0, y: "-100%"});

// start header-text animation at the same time as the previous one
timeline.from("#header-text",        {duration: .3, opacity:0, y: "100%"}, "-=0.3");

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
    for (var idx in data_fields){
        var field_name = data_fields[idx];
        if (idx in params){
            document.getElementById(field_name).querySelector("span").innerText = params[idx];
        }
    }
}

// Autoplay: comment this out in production
//document.addEventListener("DOMContentLoaded", function(){
//    play();
//}); // DOMContentLoaded
