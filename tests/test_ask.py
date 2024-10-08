import pytest
from typer.testing import CliRunner
from whisper.cli.ask import app
from unittest.mock import patch, MagicMock

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
def test_ask_command(mock_create_chain, mock_chain):
    mock_create_chain.return_value = mock_chain
    result = runner.invoke(app, ["ask", "What is the weather today?"])

    assert "Test response" in result.stdout
    assert mock_create_chain.called


@patch("whisper.cli.ask.clipboard.copy")
@patch("whisper.cli.ask.create_chain")
def test_ask_command_with_copy(mock_create_chain, mock_clipboard, mock_chain):
    mock_create_chain.return_value = mock_chain

    result = runner.invoke(app, ["ask", "What is the weather today?", "--copy"])
    mock_clipboard.assert_called_with("Test snippet")
    assert "Test response" in result.stdout
