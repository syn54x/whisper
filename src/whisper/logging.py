import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.WARN,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)

LOGGER = logging.getLogger("rich")
