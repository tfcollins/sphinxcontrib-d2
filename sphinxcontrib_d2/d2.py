"""sphinx-d2 is a Sphinx extension for the d2 diagramming language."""

from __future__ import annotations
import os
import shutil

from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.util import logging

logger = logging.getLogger(__name__)


class D2Directive(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    has_content = True

    def generate_diagram(self, content, name, alt):
        env = self.state.document.settings.env
        pagename = self.state.document.settings.env.docname
        builder = self.state.document.settings.env.app.builder

        out_filename = builder.get_outfilename(pagename)
        outdir = os.path.dirname(out_filename)
        image_dir = "_images"
        if hasattr(env.config, "html_static_path") and env.config.html_static_path:
            assert (
                len(env.config.html_static_path) == 1
            ), "Only one html_static_path is supported"
            image_dir = env.config.html_static_path[0]
        image_dir = os.path.join(outdir, image_dir)

        d2_path = env.config.d2_config.get("d2_path")
        format = env.config.d2_config.get("file_format")
        d2_args = env.config.d2_config.get("d2_args")
        if isinstance(d2_args, list):
            d2_args = " ".join(d2_args)

        document = self.state.document
        document.reporter.info("Generating d2 diagram", line=self.lineno)

        with open("diagram.d2", "w") as f:
            f.write("\n".join(content))

        # Run d2
        target = os.path.join(image_dir, f"{name}.{format}")
        result = os.system(f"{d2_path} {d2_args} diagram.d2 '{target}'")
        if result != 0:
            document.reporter.error(
                f"d2 failed with exit code {result}", line=self.lineno
            )
            return None

        # Remove the d2 file
        os.remove("diagram.d2")

        # Create image node
        if format == "svg":
            return nodes.raw(
                "",
                f"""<object data="_images/{name}.{format}" type="image/svg+xml">
            <p class="warning">{alt}</p></object>
""",
                format="html",
            )
        elif format == "png":
            return nodes.raw(
                "",
                f'<img src="_images/{name}.{format}" alt="{alt}" />',
                format="html",
            )
        elif format == "pdf":
            return nodes.raw(
                "",
                f'<object data="_images/{name}.{format}" type="application/pdf" width="100%" height="100%">'
                f'<p class="warning">{alt}</p></object>',
                format="html",
            )
        raise NotImplementedError(f"File format {format} not supported")

    def parse_content(self):
        content = self.content
        options = {}
        remaining_content = []
        for line in content:
            line = line.strip()
            if line.startswith(":"):
                if line.count(":") != 2:
                    logger.warning(f"[d2 extension] Invalid option line {line}")
                    continue
                # Reset remaining
                remaining_content = []
                # of form ":key: value"
                line = line[1:]
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                options[key] = value
            else:
                remaining_content.append(line)

        return options, remaining_content

    def run(self):
        document = self.state.document

        options, content = self.parse_content()

        # Create name
        if "name" in options:
            name = options["name"]
        else:
            ids = document.ids
            doc_name = list(ids.keys())[0]
            line_number = self.lineno
            name = f"d2_diagram_{doc_name}_{line_number}"

        # Create alt
        if "alt" in options:
            alt = options["alt"]
        else:
            alt = ""

        # Generate diagram
        diagram = self.generate_diagram(content, name, alt)
        if diagram is None:
            return []
        if "width" in options:
            wrapper_node = nodes.figure(width=options["width"])
        else:
            wrapper_node = nodes.figure()
        wrapper_node += diagram
        if "caption" in options:
            caption = nodes.caption(text=options["caption"])
            wrapper_node += caption

        return [wrapper_node]
