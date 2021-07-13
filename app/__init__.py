import os
import sys
import time
import json
import zipfile
import shutil

from nxtools import *

from .utils import process_sass, process_js, HTMLTemplate
from .manifest import process_manifest
from .watch import Watch






class TemplateBuilder():
    def __init__(self, src_dir, build_dir, dist_dir):
        self.src_root = src_dir
        self.build_root = build_dir
        self.dist_root = dist_dir

        self.template = HTMLTemplate("core/core.html")
        self.base_css = process_sass("core/core.sass")
        self.base_js = process_js("core/core.js")


    @property
    def templates(self) -> list:
        """Returns a list of templates available in the source directory"""
        return [d for d in os.listdir(self.src_root) \
            if os.path.isdir(os.path.join(self.src_root, d)) ]

    def _build(self, name: str) -> bool:
        source_dir = os.path.join(self.src_root, name)
        if not os.path.isdir(source_dir):
            logging.error(f"No such template {name}")
            return False

        tpl_html_path = os.path.join(source_dir, "template.html")
        tpl_sass_path = os.path.join(source_dir, "template.sass")
        tpl_js_path   = os.path.join(source_dir, "template.js")
        manifest_path = os.path.join(source_dir, "manifest.json")
        logging.info("Building template", name)

        #
        # Render HTML
        #

        self.template.clear()

        self.template["core_css"] = self.base_css
        self.template["core_js"] =  self.base_js

        if os.path.exists(tpl_sass_path) and os.path.getsize(tpl_sass_path):
            self.template["tpl_css"] = process_sass(tpl_sass_path)

        if os.path.exists(tpl_js_path):
            self.template["tpl_js"] = process_js(tpl_js_path)

        if os.path.exists(tpl_html_path):
            self.template["body"] = open(tpl_html_path).read()

        manifest = {}
        if os.path.exists(manifest_path):
            manifest = json.load(open(manifest_path))

        self.template["manifest"] = manifest

        param_map = "var param_map = {\n"
        for i, param in enumerate(manifest.get("parameters", [])):
            param_map += f"   'f{i}' : '{param['id']}',\n"
        param_map+= "}"

        self.template["param_map"] = param_map

        #
        # Save output files
        #

        # Create destination directory "build/template_name"
        target_dir = os.path.join(self.build_root, name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with open(os.path.join(target_dir, name + ".html"), "w") as f:
            f.write(self.template())

        with open(os.path.join(target_dir, name + ".xml"), "w") as f:
            f.write(process_manifest(manifest))

        # Copy dependencies
        for depname in os.listdir(source_dir):
            if depname in [
                    "template.html",
                    "template.sass",
                    "template.scss",
                    "template.js",
                    "manifest.json"
                    ]:
                continue
            dep_src = os.path.join(source_dir, depname)
            dep_tgt = os.path.join(target_dir, depname)
            try:
                shutil.copy(dep_src, dep_tgt)
            except Exception:
                logging.warning(f"Unable to copy {name} dependency: {depname}")
                continue

        return True


    def build(self, name:str=None, dist:bool=False) -> bool:
        if name == None:
            templates = self.templates
        elif name in self.templates:
            templates = [name]
        else:
            logging.error(f"No such template {name}")
            return False

        if not templates:
            logging.error(f"No template found")
            return False

        for template in templates:
            start_time = time.time()
            try:
                if not self._build(template):
                    continue
            except Exception:
                log_traceback(f"Building of {template} failed")
                continue

            if dist:
                logging.debug(f"Creating dist archive {template}.zip")
                tdir = os.path.join(self.build_root, template)
                zipname = os.path.join(self.dist_root, template + ".zip")
                with zipfile.ZipFile(zipname, "w") as z:
                    for folder_name, subfolders, filenames in os.walk(tdir):
                        for filename in filenames:
                            filePath = os.path.join(folder_name, filename)
                            z.write(filePath, os.path.basename(filePath))

            logging.goodnews(f"Building of {template} finished in {time.time() - start_time:.03f}s")
        return True


    def watch(self, name:str=None, dist:bool=False) -> bool:
        def handler(event):
            r = set()
            for path in event:
                try:
                    chname, fname = path.replace("\\", "/").split("/")[-2:]
                except ValueError:
                    continue
                if name is None or name == chname:
                    logging.debug(f"{fname} has been changed. Rebuilding {chname}")
                    self.build(name, dist=dist)


        w = Watch(self.src_root, handler)
        w.start()



