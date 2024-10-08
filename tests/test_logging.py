import logging
from whisper.logging import LOGGER


def test_logger_instance():
    assert isinstance(LOGGER, logging.Logger)
    assert LOGGER.name == "rich"


def test_logger_level():
    assert LOGGER.level == logging.WARN


def test_logger_handler():
    assert len(LOGGER.handlers) == 1
    handler = LOGGER.handlers[0]
    assert isinstance(handler, logging.Handler)
    assert handler.__class__.__name__ == "RichHandler"


def test_logger_formatting():
    formatter = LOGGER.handlers[0].formatter
    assert formatter._fmt == "%(message)s"


def test_logging_output(caplog):
    test_message = "This is a test warning"
    LOGGER.warning(test_message)
    assert test_message in caplog.text


def test_logging_levels(caplog):
    debug_message = "This is a debug message"
    info_message = "This is an info message"
    warning_message = "This is a warning message"
    error_message = "This is an error message"

    LOGGER.debug(debug_message)
    LOGGER.info(info_message)
    LOGGER.warning(warning_message)
    LOGGER.error(error_message)

    assert debug_message not in caplog.text
    assert info_message not in caplog.text
    assert warning_message in caplog.text
    assert error_message in caplog.text
