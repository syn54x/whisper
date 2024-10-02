import pytest
from unittest.mock import patch, MagicMock
import markdown
from xml.etree.ElementTree import Element
from whisper.mkdocs_typer import TyperExtension, TyperPattern, MkdocsTyper


@pytest.fixture
def mock_match():
    mock_match = MagicMock()
    mock_match.start.return_value = 0
    mock_match.end.return_value = 11
    yield mock_match


def test_typer_extension_initialization():
    md = markdown.Markdown()
    extension = TyperExtension(cmd="echo 'Hello World'")
    extension.extendMarkdown(md)
    assert isinstance(md.inlinePatterns["typer"], TyperPattern)


@patch("subprocess.run")
def test_typer_pattern_handle_match_success(mock_run, mock_match):
    mock_run.return_value = MagicMock(returncode=0, stdout="Hello World")

    pattern = TyperPattern("::typer", cmd="echo 'Hello World'")
    md = markdown.Markdown()

    node, start, end = pattern.handleMatch(mock_match, md)

    assert isinstance(node, Element)
    assert "Hello World" in node.find("p").text


@patch("subprocess.run")
def test_typer_pattern_handle_match_failure(mock_run, mock_match):
    mock_run.return_value = MagicMock(returncode=1, stdout="Error")
    pattern = TyperPattern("::typer", cmd="echo 'Hello World'")
    md = markdown.Markdown()
    result = pattern.handleMatch(mock_match, md)
    assert result == (None, 0, 11)


def test_mkdocs_typer_on_config():
    plugin = MkdocsTyper()
    plugin.config["cmd"] = "echo 'Hello World'"
    config = {"markdown_extensions": []}
    plugin.on_config(config)
    assert any(isinstance(ext, TyperExtension) for ext in config["markdown_extensions"])
