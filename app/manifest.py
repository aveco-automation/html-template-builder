def process_manifest(manifest:dict) -> str:
    """ Convert a JSON manifest to CasparCG compatible XML
    """

    tpl_header_data = {
        "version" : "2.0.0",
        "author_name" : manifest.get("author_name", "Nebula Broadcast"),
        "author_email" : manifest.get("author_email", "info@nebulabroadcast.com"),
        "template_info" : "",
        "width" : manifest.get("width", 1920),
        "height" : manifest.get("height", 1080),
        "frame_rate" : manifest.get("frame_rate", 50),
    }

    tplinfo = "<template"
    tplinfo += " version=\"{version}\""
    tplinfo += " authorName=\"{author_name}\""
    tplinfo += " authorEmail=\"{author_email}\""
    tplinfo += " templateInfo=\"{template_info}\""
    tplinfo += " originalWidth=\"{width}\""
    tplinfo += " originalHeight=\"{height}\""
    tplinfo += " originalFrameRate=\"{frame_rate}\">\n"

    tplinfo = tplinfo.format(**tpl_header_data)

    tplinfo += "  <components/>\n"
    tplinfo += "  <keyframes/>\n"
    tplinfo += "  <instances/>\n"

    tplinfo += "  <parameters>\n"
    for param in manifest.get("parameters", []):
        param["type"] = param.get("type" , "string")
        param["info"] = param.get("info" , "")

        attrs = " ".join([f"{k}=\"{v}\"" for k,v in param.items() if v  ])
        tplinfo += f"    <parameter {attrs}/>\n"

    tplinfo += "  </parameters>\n"
    tplinfo += "</template>\n"
    return tplinfo

