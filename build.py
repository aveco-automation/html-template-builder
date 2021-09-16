#!/usr/bin/env python3

import pathlib
import threading
import typer
import time
import http.server
import socketserver

from nxtools import logging
from app import TemplateBuilder

logging.show_time = True
app = typer.Typer(add_completion=False)

dir_checks = {
    "exists" : True,
    "file_okay" : False,
    "dir_okay" : True
}

@app.command()
def build(
        watch:bool=typer.Option(False, help="Watch the source directory and rebuild templates when source files are changed"),
        serve:bool=typer.Option(False, help="Same as --watch, but additionally run a web server"),
        dist:bool=typer.Option(False, help="Also generate zip files containing finished template(s)"),
        template:str=typer.Option(None, help="When specified, build/watch only the selected template and ignore the rest"),
        src_dir:pathlib.Path=typer.Option("./src", help="Path to the source root directory", **dir_checks),
        build_dir:pathlib.Path=typer.Option("./build", help="Path to the output directory", **dir_checks),
        dist_dir:pathlib.Path=typer.Option("./dist", help="Path to the directory where resulting zip files will be stored", **dir_checks)
        ):
    """
    HTML Template Builder 1.1.0

    For detailed instructions, see the README.md file or visit
    https://github.com/aveco-automation/html-template-builder

    (c) 2020 - 2021, Aveco inc., imm studios, z.s.

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License along with this program.
    If not, see https://www.gnu.org/licenses.

    """

    builder = TemplateBuilder(src_dir=src_dir, build_dir=build_dir, dist_dir=dist_dir)

    builder.build(template, dist=dist)
    if watch or serve:

        # start builder.watch in a separate thread
        thread = threading.Thread(target=builder.watch, kwargs={"dist" : dist})
        thread.start()

        
        if serve:
            #TODO: much much smarter http handler. with index and stuff...
            class Handler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=str(build_dir), **kwargs)

            with socketserver.TCPServer(("", 8000), Handler) as httpd:
                logging.info("Serving at http://localhost:8000/")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    httpd.shutdown()
                    builder.watcher.stop()
                    logging.info("\n\nExiting...")

            # Wait for the webserver to shut down
            time.sleep(1)
        else:
            while True:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    builder.watcher.stop()
                    break
        



if __name__ == '__main__':
    print()
    app()

