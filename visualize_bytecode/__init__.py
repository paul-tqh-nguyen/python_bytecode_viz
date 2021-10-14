import os
import shutil
import json

from .process_bytecode import function_cfg_to_dict

from typing import Callable

_MODULE_DIR = os.path.abspath(os.path.dirname(__file__))

VISUALIZATION_HTML_LOCATION = os.path.join(
    _MODULE_DIR, "web_templates", "visualization.html"
)
VISUALIZATION_CSS_LOCATION = os.path.join(
    _MODULE_DIR, "web_templates", "visualization.css"
)
VISUALIZATION_JS_LOCATION = os.path.join(
    _MODULE_DIR, "web_templates", "visualization.js"
)


def visualize_bytecode(func: Callable, output_dir: str) -> None:
    output_dir = os.path.abspath(output_dir)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    shutil.copy(VISUALIZATION_HTML_LOCATION, output_dir)
    shutil.copy(VISUALIZATION_CSS_LOCATION, output_dir)

    json_dict = function_cfg_to_dict(func)
    with open(VISUALIZATION_JS_LOCATION, "r") as f:
        lines = f.readlines()
        assert lines[0] == "const data;\n"
        json_data_string = json.dumps(json_dict, sort_keys=True, indent=4)
        # bake the data into the JS code to avoiid CORS issues.
        lines[0] = "const data = " + json_data_string + ";\n"
        js_code = "".join(lines)

    output_js_location = os.path.basename(VISUALIZATION_JS_LOCATION)
    output_js_location = os.path.join(output_dir, output_js_location)
    with open(output_js_location, "w") as f:
        f.write(js_code)

    return
