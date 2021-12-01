// To specify an image to be displayed, you may either use a full path (remote or local)
// to the image, or use a "c:\\fakepath\\" prefix.
// c:\\fakepath\\ will be replaced with the path to the pictureFolder, which is
// specified in the configuration file (config.js).

// This is basically what CGManager does - in its preview mode, it uses a HTTP address
// to point to its server endpoint returning the image, but when creating a MOS item,
// it uses c:\\fakepath\\ prefix, so when played by CasparCG, it will use the image
// from the local filesystem.

// Then the local file may be played back in CasparCG by using the following AMCP command.
// Since a double backlash character is used, escaping is a little bit ridiculous:
//
// CG 1-10 ADD 0 example-image/example-image 0 "{\"image\": \"c:\\\\\\\\fakepath\\\\\\\\image.png\"}"
// CG 1-10 PLAY 0


function get_image_url(raw) {
    if (raw.substr(0, 12).toUpperCase() == "C:\\FAKEPATH\\") {
        raw = picturePath + raw.substr(12);
    }
    return raw;
}

function play() {
    document.getElementById("container").setAttribute("class", "visible");
}

function stop() {
    document.getElementById("container").setAttribute("class", "hidden");
}


function update(data) {
    const params = parse_params(data)
    for (var field_name in params) {
        console.log(field_name + ": " + params[field_name])
        if (field_name == "image") {
            const image_url = get_image_url(params[field_name])
            document.getElementById("image").src = image_url
            console.log("IMAGE: " + image_url)
        }
    }
}