import pytest
from typer.testing import CliRunner
from whisper.config import app

runner = CliRunner()


@pytest.fixture
def mock_user_config(mocker):
    mocker.patch("whisper.config.UserConfig.save")
    return mocker.patch("whisper.config.UserConfig")


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
