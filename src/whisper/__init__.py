from .cli.ask import app
from .cli.config import app as config_app

import time
import random

from rich.live import Live
from rich.table import Table
from rich.panel import Panel


def generate_table() -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("ID")
    table.add_column("Value")
    table.add_column("Status")

    for row in range(random.randint(2, 6)):
        value = random.random() * 100
        table.add_row(
            f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS"
        )
    return table


@app.command()
def table():
    with Live(generate_table(), refresh_per_second=4) as live:
        for _ in range(40):
            time.sleep(0.4)
            live.update(Panel(generate_table()))


app.add_typer(config_app, name="config")

if __name__ == "__main__":
    app()
