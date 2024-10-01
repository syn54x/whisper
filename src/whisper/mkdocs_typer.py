import subprocess
import markdown
import xml.etree.ElementTree as etree

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from markdown.inlinepatterns import InlineProcessor


class TyperExtension(markdown.Extension):
    def __init__(self, *args, cmd: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmd = cmd

    def extendMarkdown(self, md):
        # Register the new pattern to handle ::typer
        md.inlinePatterns.register(
            TyperPattern(r"::typer", md, cmd=self.cmd), "typer", 175
        )


class TyperPattern(InlineProcessor):
    def __init__(self, *args, cmd: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmd = cmd

    def handleMatch(self, m, data):
        result = subprocess.run(self.cmd.split(" "), capture_output=True, text=True)

        if result.returncode == 0:
            html_output = markdown.markdown(result.stdout)
            return etree.fromstring(f"<div>{html_output}</div>"), m.start(0), m.end(0)
        else:
            return None, m.start(0), m.end(0)


def makeExtension(**kwargs):
    return TyperExtension(**kwargs)


class MkdocsTyper(BasePlugin):
    config_scheme = (
        (
            "cmd",
            config_options.Type(str, default="typer whisper utils docs --name Whisper"),
        ),
    )

    def on_config(self, config):
        """Called after the configuration is loaded."""
        # Add the updated Markdown extension to the list
        config["markdown_extensions"].append(makeExtension(cmd=self.config["cmd"]))
        return config

    def on_pre_build(self, config):
        """Called before the MkDocs build process starts."""
        pass
