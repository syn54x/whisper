from .cli.ask import app
from .cli.config import app as config_app

app.add_typer(config_app, name="config")

if __name__ == "__main__":
    app()
