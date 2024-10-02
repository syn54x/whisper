import pytest
from typer.testing import CliRunner
from whisper import app
from unittest.mock import patch
from rich.console import Console

runner = CliRunner()


@pytest.fixture
def mock_console():
    with patch.object(Console, "print") as mock_print:
        yield mock_print


def test_themes_command(mock_console):
    result = runner.invoke(app, ["themes"])
    assert result.exit_code == 0
    # Check if the print method was called at least once
    assert mock_console.called
    # You can further check for specific themes if you want to be very precise
    args, kwargs = mock_console.call_args
    print(dir(args))
    output = str(args[0])
    assert "solarized-dark" in output
    assert "monokai" in output  # Assuming 'monokai' is a part of the themes
