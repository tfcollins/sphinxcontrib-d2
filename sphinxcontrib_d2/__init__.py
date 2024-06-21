"""Sphinx extension for the d2 diagramming language."""
import shutil
import os

from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata

from sphinx.util import logging

from .d2 import D2Directive

__version__ = "0.1.0"

logger = logging.getLogger(__name__)


def on_config_inited(app: Sphinx, config: dict) -> None:
    """Called when the configuration is initialized."""
    d2_config = config.d2_config

    # Make sure d2 executable is there
    if not d2_config.get("d2_path"):
        if os.name == "posix":
            d2_executable = shutil.which("d2")
        elif os.name == "nt":
            d2_executable = shutil.which("d2.exe")
        else:
            logger.error(f"OS {os.name} not supported")
            raise NotImplementedError(f"OS {os.name} not supported")
    else:
        if os.path.exists(d2_config["d2_path"]):
            d2_executable = d2_config["d2_path"]
        else:
            logger.error(f"d2 executable not found at {d2_config['d2_path']}")
            raise FileNotFoundError(
                f"d2 executable not found at {d2_config['d2_path']}"
            )

    d2_config["d2_path"] = d2_executable

    if "file_format" not in d2_config:
        d2_config["file_format"] = "svg"
    assert d2_config["file_format"] in [
        "svg",
        "png",
    ], "file_format must be 'svg' or 'png'"

    if "d2_args" not in d2_config:
        d2_config["d2_args"] = ""

    config.d2_config = d2_config


def setup(app: Sphinx) -> ExtensionMetadata:

    # Add configuration values
    app.add_config_value("d2_config", {}, "env")
    app.connect("config-inited", on_config_inited)

    # Add directives
    app.add_directive("d2", D2Directive)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
