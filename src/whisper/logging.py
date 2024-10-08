import logging
from rich.logging import RichHandler

LOGGER = logging.getLogger("rich")

LOGGER.setLevel(logging.WARN)
rich_handler = RichHandler(rich_tracebacks=True, markup=True)
rich_handler.setFormatter(logging.Formatter("%(message)s"))
LOGGER.addHandler(rich_handler)
