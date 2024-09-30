import typer
from rich.pretty import pprint
from .settings import UserConfig

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
