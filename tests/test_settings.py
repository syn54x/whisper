import pytest
from unittest.mock import patch
from pydantic_settings import SettingsConfigDict
from pathlib import Path
from whisper.settings import UserConfig, make_local_path


@pytest.fixture
@patch("whisper.settings.platform.system")
def expected_toml(mock_system):
    mock_system.return_value = "Darwin"
    return f"""[default]
provider = "openai"
theme = "solarized-dark"

[gpt4all]
local_path = "{make_local_path()}"
local_model = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

[openai]
api_key = "replace-me"
model = "gpt-3.5-turbo"

[anthropic]
api_key = "replace-me"
model = "claude-3-5-sonnet-20240620"

[mistral]
api_key = "replace-me"
model = "pixtral-12b-2409"

[fireworks]
api_key = "replace-me"
model = "accounts/fireworks/models/llama-v3p1-405b-instruct"

[azureopenai]
api_key = "replace-me"
model = "gpt-4o"
"""


@pytest.fixture
def user_config(tmp_path):
    config_path = tmp_path / ".whisper"
    config_path.mkdir()
    config_file = config_path / "whisper.toml"
    config_file.write_text("""
    [default]
    copy_snippet = true
    provider = "openai"
    theme = "solarized-dark"

    [gpt4all]
    local_path = "/Users/markjtaylorroberts/Library/Application Support/nomic.ai/GPT4All"
    local_model = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

    [openai]
    api_key = "test-api-key"
    model = "gpt-3.5-turbo"
    """)

    class MockUserConfig(UserConfig):
        model_config = SettingsConfigDict(toml_file=[str(config_file)])

    return MockUserConfig()


def test_load_user_config(user_config):
    assert user_config.default.copy_snippet
    assert user_config.openai.api_key == "test-api-key"


def test_save_user_config(tmp_path, user_config):
    user_config.openai.api_key = "new-api-key"
    user_config.save()
    config_path = Path(user_config.model_config["toml_file"][0])
    assert config_path.read_text().find("new-api-key") != -1


def test_dot_notation_access(user_config):
    assert user_config.get_by_dot_notation("openai.api_key") == "test-api-key"
    user_config.set_by_dot_notation("openai.api_key", "updated-api-key")
    assert user_config.openai.api_key == "updated-api-key"


def test_config_exists(user_config):
    assert user_config.config_exists()


@patch("whisper.settings.platform.system")
def test_initialize(mock_system, user_config, expected_toml):
    mock_system.return_value = "Darwin"
    toml = user_config.initialize()

    assert toml == expected_toml
