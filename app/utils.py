"""HTML builder utilities."""

import os
import jinja2
import htmlmin
import jsmin
import sass


class HTMLTemplate():
    """HTML template builder."""

    def __init__(self):
        """Initialize the template."""
        with open("core/core.html") as f:
            self.template = jinja2.Template(f.read())
        self.clear()

    def clear(self):
        """Clear the context."""
        self.ctx = {}

    def __setitem__(self, key, value):
        """Set a variable in the context."""
        self.ctx[key] = value

    def __call__(self):
        """Render the template with the context."""
        result = self.template.render(**self.ctx)
        return htmlmin.minify(
                result,
                remove_comments=True,
                remove_empty_space=True,
                remove_optional_attribute_quotes=False
            )


#
# Minifiers
#


def process_js(source_path: str) -> str:
    """Return a minified javascript file.

    Returns empty string if the path does not exist.

    Args:
        source_path (str): Path to the source js file

    Returns:
        str: Minified version of the script
    """
    try:
        with open(source_path) as js_file:
            minified = jsmin.jsmin(js_file.read())
            return minified
    except Exception:
        return ""


def process_sass(source_path: str) -> str:
    """Return a minified sass script.

    Returns empty string if the path does not exist.

    Args:
        source_path (str): Path to the source sass file

    Returns:
        str: Resulting minified CSS
    """
    with open(source_path) as sass_file:
        minified = sass.compile(
                string=sass_file.read(),
                indented=os.path.splitext(source_path)[1] == ".sass",
                output_style="compressed"
            )
        return minified
