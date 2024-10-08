import logging
import sys
import typer
import clipboard
from typing import Annotated
from rich.console import Console

from ..settings import config
from ..chains import create_chain
from ..logging import LOGGER
from .custom_typer import Typer

app = Typer()


@app.command(default=True)
def ask(
    prompt: Annotated[
        str,
        typer.Argument(
            help="The question you want to ask Whisper",
            default_factory=lambda: sys.stdin.read(),
        ),
    ],
    conf: Annotated[
        str,
        typer.Option(
            "-c", "--config", help="The config to be used (openai, anthropic, etc)"
        ),
    ] = None,
    system: Annotated[
        str,
        typer.Option(
            "-s",
            "--system",
            help="The system prompt to be used.  This can also be piped into Whisper...",
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
    verbosity: Annotated[
        int,
        typer.Option("-v", "--verbose", help="Increase verbosity level", count=True),
    ] = 0,
):
    """
    The default command that takes a prompt and optional parameters to ask a question using Whisper.
    """

    LOGGER.setLevel(logging.DEBUG if verbosity >= 2 else logging.INFO)

    system = (
        system
        or "You are an AI assistant that can answer questions and help with tasks."
    )

    console = Console(color_system="auto")

    LOGGER.info("Running whisper ask...")
    LOGGER.debug(f"[bold]Using config:[/bold] {conf}")
    LOGGER.debug(f"[bold]Using model:[/bold] {model}")
    LOGGER.debug(f"[bold]Using theme:[/bold] {theme}")
    LOGGER.debug(f"[bold]Using system prompt:[/bold] {system}")
    LOGGER.debug(f"[bold]Using prompt:[/bold] {prompt}")

    with console.status("Thinking...", spinner="dots"):
        chain = create_chain(conf, model)
        result = chain.invoke({"system_prompt": system, "context": prompt})

    if copy is not None:
        if copy and result.snippet:
            clipboard.copy(result.snippet)
    elif config.default.copy_snippet and result.content:
        clipboard.copy(result.content)

    panel = result.render(theme)
    console.print(panel)
