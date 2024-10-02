from pydantic_core import ValidationError

try:
    import typer
    import clipboard
    from typing import Annotated
    from pathlib import Path
    from rich.console import Console
    from rich.pretty import pprint
    from rich import print
    from pygments.styles import get_all_styles

    from .settings import UserConfig
    from .custom_typer import Typer
    from .chains import create_chain
    from .config import app as config_app

    config = UserConfig()

except ValidationError:
    print("[red]Please run `whisper init` to initialize the configuration.[/red]")

app = Typer()


@app.command(default=True)
def ask(
    prompt: Annotated[str, typer.Argument(help="The question you want to ask Whisper")],
    key: Annotated[
        str, typer.Option("-k", "--key", help="The API To use (openai, anthropic, etc)")
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
        chain = create_chain(key, model)
        result = chain.invoke({"context": prompt})

    if copy is not None:
        if copy and result.snippet:
            clipboard.copy(result.snippet)
    elif config.default.copy and result.content:
        clipboard.copy(result.content)

    panel = result.render(theme)
    console.print(panel)


@app.command()
def themes():
    """Prints a list of available syntax highlighting themes from Pygments."""
    pprint(list(get_all_styles()))


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
    config_path = Path.home() / ".whisper"
    config_path.mkdir(parents=True, exist_ok=True)
    config_file = config_path / "whisper.toml"

    with config_file.open("w") as f:
        toml_str = UserConfig.initialize(openai_key, anthropic_key)
        f.write(toml_str)

    if show:
        print(toml_str)

    print(f"Initialized whisper configuration in {config_file}")


app.add_typer(config_app, name="config")

if __name__ == "__main__":
    app()
