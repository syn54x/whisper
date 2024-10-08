import pytest
from typer.testing import CliRunner
from rich.console import Console
from unittest.mock import patch


from whisper.cli.config import app

runner = CliRunner()


@pytest.fixture
def mock_user_config(mocker):
    mocker.patch("whisper.cli.config.UserConfig.save")
    return mocker.patch("whisper.cli.config.UserConfig")


def test_set_command(mock_user_config):
    runner.invoke(app, ["set", "openai.api_key", "new-api-key"])
    mock_user_config.return_value.set_by_dot_notation.assert_called_once_with(
        "openai.api_key", "new-api-key"
    )
    mock_user_config.return_value.save.assert_called_once()


def test_show_command(mock_user_config):
    mock_user_config.return_value.__str__.return_value = "config content"
    runner.invoke(app, ["show"])


def test_get_command(mock_user_config):
    mock_user_config.return_value.get_by_dot_notation.return_value = "some-value"
    runner.invoke(app, ["get", "openai.api_key"])
    mock_user_config.return_value.get_by_dot_notation.assert_called_once_with(
        "openai.api_key"
    )


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
