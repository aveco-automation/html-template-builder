function play(){
    document.getElementById("container").setAttribute("class", "visible");
}

function stop(){
    document.getElementById("container").setAttribute("class", "hidden");
}

function update(data){
    var params = parse_params(data);
    for (var field_name in params){
        document.getElementById(field_name).querySelector("span").innerText = params[field_name];
    }
}

// Autoplay: comment this out in production
//document.addEventListener("DOMContentLoaded", function(){
//    play();
//}); // DOMContentLoaded
