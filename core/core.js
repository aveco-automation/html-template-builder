var debug = false;

function log(s) {
    console.log(s)
    if (debug) {
        const li = document.createElement('li');
        li.innerText = s;
        dbg = document.getElementById("debug-window");
        dbg.appendChild(li);
    }
}

window.onerror = function(msg) {
    log('error ' + msg);
}

function parse_xml(xmlString) {
    var parser = new DOMParser();
    var docError = parser.parseFromString('INVALID', 'text/xml');
    var parsererrorNS = docError.getElementsByTagName("parsererror")[0].namespaceURI;
    var doc = parser.parseFromString(xmlString, 'text/xml');
    if (doc.getElementsByTagNameNS(parsererrorNS, 'parsererror').length > 0) {
        throw new Error('Error parsing XML');
    }
    return doc;
}

function parse_params(str){
    var data = {};
    try {
        data = JSON.parse(str)
    } catch (err) {
        try {
            doc = parse_xml(str);
            var result = {};
            var root_element = doc.documentElement;
            var children = root_element.childNodes;
            for(var i =0 ; i < children.length; i++) {
                var child = children[i];
                var key = child.getAttribute("id");
                var data = child.getElementsByTagName("data")[0];
                var value = data.getAttribute("value");
                result[key] = value;
            }
            data = result
        } catch (xmlerr) {
            data = {}
        }
    }
    for (k in data){
        if (k in param_map){
            data[param_map[k]] = data[k]
            delete data[k]
        }
    }
    console.log(data)
    return data
}

function play() {}
function stop() {}
function next() {}
function update(data) {}


var amcp_bridge_url = "http://127.0.0.1:9731/amcp"
var amcp_bridge_timeout = 5000

function amcp(command){
    return new Promise(function(resolve, reject){

        log("AMCP TX: " + command)

        var xhr = new XMLHttpRequest()
        xhr.timeout = amcp_bridge_timeout
        xhr.open('POST', amcp_bridge_url)
        xhr.responseType = "text"
        xhr.send(command)

        xhr.onload = function() {
            log("AMCP RX: " + xhr.status + " " + command)
            if (xhr.status < 400)
                resolve(xhr.status, xhr.responseText)
            else
                reject(xhr.status, xhr.responseText)
        };

        xhr.onerror = function() {
            log("AMCP RX ERR:", xhr.status)
            reject(xhr.status, xhr.responseTextx)
        }

    }) // return new Promise
}
