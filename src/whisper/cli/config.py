import typer
from typing import Annotated
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.text import Text
from pygments.styles import get_all_styles
from rich.pretty import pprint

from ..chains import CodeWhisper
from ..settings import config, UserConfig

app = typer.Typer()


@app.command()
def set(
    key: str = typer.Argument(
        ...,
        help="The key to set the value for.  Supports dot notation.  e.g. 'openai.api_key'",
    ),
    value: str = typer.Argument(..., help="The value to set the key to."),
):
    """
    Initialize the configuration for Whisper.
    """
    config = UserConfig()
    config.set_by_dot_notation(key, value)
    config.save()

    pprint(config)


@app.command()
def show():
    """
    Show the current configuration for Whisper.
    """
    config = UserConfig()
    pprint(config)


@app.command()
def get(
    key: str = typer.Argument(
        ...,
        help="The key to get the value for.  Supports dot notation.  e.g. 'openai.api_key'",
    ),
):
    """
    Get the current configuration for Whisper.
    """
    config = UserConfig()

    typer.echo(config.get_by_dot_notation(key))


@app.command()
def themes():
    """Prints a list of available syntax highlighting themes from Pygments."""
    console = Console()
    console.print(Text(", ".join(list(get_all_styles())), style="bold green"))


@app.command()
def init(
    openai_key: str = typer.Option(
        None, "--openai-key", help="The OpenAI API key to use"
    ),
    anthropic_key: str = typer.Option(
        None, "--anthropic-key", help="The Anthropic API key to use"
    ),
    azureopenai_key: str = typer.Option(
        None, "--azureopenai-key", help="The Azure OpenAI API key to use"
    ),
    mistral_key: str = typer.Option(
        None, "--mistral-key", help="The Mistral API key to use"
    ),
    fireworks_key: str = typer.Option(
        None, "--fireworks-key", help="The Fireworks API key to use"
    ),
    show: Annotated[
        bool, typer.Option("--show/--no-show", help="Show the configuration")
    ] = True,
):
    """
    Initializes the configuration for Whisper, saving API keys to a local file.
    """
    console = Console()
    config_path = Path.home() / ".whisper"
    config_path.mkdir(parents=True, exist_ok=True)
    config_file = config_path / "whisper.toml"

    with config_file.open("w") as f:
        toml_str = UserConfig.initialize(
            openai_key, anthropic_key, mistral_key, fireworks_key, azureopenai_key
        )
        f.write(toml_str)

    if show:
        syntax = Syntax(toml_str, "toml", theme=config.default.theme, padding=1)
        panel = CodeWhisper.render_syntax(syntax, "Whisper Configuration")
        console.print(panel)

    console.print(f"[green]Initialized whisper configuration in {config_file}[/green]")
