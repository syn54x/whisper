import typer
import clipboard
from typing import Annotated
from rich.console import Console

from ..settings import config
from ..chains import create_chain
from .custom_typer import Typer

app = Typer()


@app.command(default=True)
def ask(
    prompt: Annotated[str, typer.Argument(help="The question you want to ask Whisper")],
    conf: Annotated[
        str,
        typer.Option(
            "-c", "--config", help="The config to be used (openai, anthropic, etc)"
        ),
    ] = None,
    model: Annotated[
        str, typer.Option("-m", "--model", help="The model that Whisper should use")
    ] = None,
    theme: Annotated[
        str,
        typer.Option(
            "-t", "--theme", help="The theme that should be used for the output"
        ),
    ] = "solarized-dark",
    copy: Annotated[
        bool, typer.Option("--copy/--no-copy", help="Copy the output to the clipboard")
    ] = None,
):
    """
    The default command that takes a prompt and optional parameters to ask a question using Whisper.
    """
    console = Console(color_system="auto")

    with console.status("Thinking...", spinner="dots"):
        chain = create_chain(conf, model)
        result = chain.invoke({"context": prompt})

    if copy is not None:
        if copy and result.snippet:
            clipboard.copy(result.snippet)
    elif config.default.copy_snippet and result.content:
        clipboard.copy(result.content)

    panel = result.render(theme)
    console.print(panel)
