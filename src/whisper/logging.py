import logging
from rich.logging import RichHandler

# logging.basicConfig(
#     level=logging.WARN,
#     format="%(message)s",
#     datefmt="[%X]",
#     handlers=[RichHandler(rich_tracebacks=True, markup=True)],
# )

LOGGER = logging.getLogger("rich")

LOGGER.setLevel(logging.WARN)
rich_handler = RichHandler(rich_tracebacks=True, markup=True)
rich_handler.setFormatter(logging.Formatter("%(message)s"))
LOGGER.addHandler(rich_handler)
