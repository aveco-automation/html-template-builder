HTML Template builder
=====================

![GitHub release (latest by date)](https://img.shields.io/github/v/release/aveco-automation/html-template-builder?style=for-the-badge)
![Maintenance](https://img.shields.io/maintenance/yes/2021?style=for-the-badge)
![Last commit](https://img.shields.io/github/last-commit/aveco-automation/html-template-builder?style=for-the-badge)
![Python version](https://img.shields.io/badge/python-3.6-blue?style=for-the-badge)

Template builder is a simple tool that assembles HTML snippet, SASS stylesheet, and JavaScript file
into a graphic template for CasparCG, or another HTML-enabled playout server.

It aims to be as simple as possible, it does not use any JS framework and does not need several gigabytes of node dependencies.


Installation
------------

To run the software from source, Python 3.6 must be installed. You also need pip to install third-party libraries.

### Linux

Clone this repository and install the required python libraries using the following command:

```
pip3 install -r requirements.txt
```

### Windows

Use the same procedure as with Linux or download the latest binary package from the releases page.

Usage
-----

### Template source

For each template, create a directory in the source root (defaults to `./src`).
The name of the directory is the template name.
In the template directory, create the following files:

#### manifest.json

Template manifest provides metadata, information about editable fields, and external javascript requirements.

Using a js element in the manifest you can specify additional javascript files to be used in the resulting template.
Specified files/URLs will be linked using `<script>` tags in the HTML header.

#### template.html

HTML snippet which will be added to the template body

#### template.sass

SASS file will be compiled to CSS and will be embedded (along with base style) to the resulting HTML file.
Base stylesheet (core/core.sass) is always included first and resolves page transparency, box-sizing,
margins, body overflow, and so on.

#### template.js

Custom javascript


### Additional files

Along with template source files and the manifest, a template directory may contain additional files,
such as javascript libraries, images, etc.

Builder copies these files automatically to the `build` folder.


### Building

Run build.py (build.exe) without arguments to build all templates in the source root directory and exit.

You may also pass the following additional parameters:

```
--watch / --no-watch   Watch the source directory and rebuild templates when
                       source files are changed  [default: False]

--dist / --no-dist     Also generate zip files containing finished
                       template(s)  [default: False]

--template TEXT        When specified, build/watch only the selected
                       template and ignore the rest

--src-dir DIRECTORY    Path to the source root directory  [default: ./src]
--build-dir DIRECTORY  Path to the output directory  [default: ./build]
--dist-dir DIRECTORY   Path to the directory where resulting zip files will
                       be stored  [default: ./dist]

--help                 Show this message and exit.
```


Legal
-----

### Credits

*html-template-builder* is originally a development by
[imm studios, z.s.](https://imm.cz) and [Aveco inc](https://aveco.com).

### License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

### Acknowledgements

This software uses the following third-party open source Python libraries:

 - [nxtools](https://pypi.org/projects/nxtools/) released under MIT license
 - [htmlmin](https://pypi.org/project/htmlmin/) released under BSD license
 - [jsmin](https://pypi.org/project/jsmin/) released under MIT license
 - [jinja2](https://pypi.org/project/jinja2/) released under BSD license
 - [libsass](https://pypi.org/project/libsass/) released under MIT license
 - [typer](https://pypi.org/project/typer/) released under MIT license
 - [python-watchdog](https://pypi.org/project/watchdog/) released under Apache Software license
