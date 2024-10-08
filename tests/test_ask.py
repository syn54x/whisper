import pytest
from typer.testing import CliRunner
from whisper.cli.ask import app
from unittest.mock import patch, MagicMock
import logging

runner = CliRunner()


@pytest.fixture
def mock_chain():
    chain = MagicMock()
    chain.invoke.return_value = MagicMock(
        content="Test response", snippet="Test snippet"
    )
    chain.invoke.return_value.render.return_value = "Test response\n"
    yield chain


@patch("whisper.cli.ask.create_chain")
@patch("whisper.cli.ask.LOGGER")
def test_ask_command(mock_logger, mock_create_chain, mock_chain):
    mock_create_chain.return_value = mock_chain
    result = runner.invoke(app, ["ask", "What is the weather today?"])

    assert "Test response" in result.stdout
    assert mock_create_chain.called
    mock_logger.info.assert_called_with("Running whisper ask...")
    mock_logger.debug.assert_called()


@patch("whisper.cli.ask.clipboard.copy")
@patch("whisper.cli.ask.create_chain")
@patch("whisper.cli.ask.LOGGER")
def test_ask_command_with_copy(
    mock_logger, mock_create_chain, mock_clipboard, mock_chain
):
    mock_create_chain.return_value = mock_chain

    result = runner.invoke(app, ["ask", "What is the weather today?", "--copy"])
    mock_clipboard.assert_called_with("Test snippet")
    assert "Test response" in result.stdout
    mock_logger.info.assert_called_with("Running whisper ask...")
    mock_logger.debug.assert_called()


@patch("whisper.cli.ask.create_chain")
@patch("whisper.cli.ask.LOGGER")
def test_ask_command_with_options(mock_logger, mock_create_chain, mock_chain):
    mock_create_chain.return_value = mock_chain
    result = runner.invoke(
        app,
        [
            "ask",
            "What is the weather today?",
            "--config",
            "openai",
            "--system",
            "You are a weather expert",
            "--model",
            "gpt-4",
            "--theme",
            "monokai",
            "-vv",
        ],
    )

    assert "Test response" in result.stdout
    assert mock_create_chain.called
    mock_create_chain.assert_called_with("openai", "gpt-4")
    mock_chain.invoke.assert_called_with(
        {
            "system_prompt": "You are a weather expert",
            "context": "What is the weather today?",
        }
    )
    mock_logger.setLevel.assert_called_with(logging.DEBUG)
    mock_logger.info.assert_called_with("Running whisper ask...")
    mock_logger.debug.assert_called()


@patch("whisper.cli.ask.create_chain")
@patch("whisper.cli.ask.LOGGER")
def test_ask_command_verbosity(mock_logger, mock_create_chain, mock_chain):
    mock_create_chain.return_value = mock_chain
    runner.invoke(app, ["ask", "Test", "-v"])
    mock_logger.setLevel.assert_called_with(logging.INFO)

    runner.invoke(app, ["ask", "Test", "-vv"])
    mock_logger.setLevel.assert_called_with(logging.DEBUG)
