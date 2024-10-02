import typer
import clipboard
from typing import Annotated
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.text import Text
from pygments.styles import get_all_styles

from .custom_typer import Typer
from .chains import create_chain, CodeWhisper
from .config import app as config_app
from .settings import config, UserConfig


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


app.add_typer(config_app, name="config")

if __name__ == "__main__":
    app()
