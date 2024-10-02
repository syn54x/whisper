from pydantic_settings import SettingsConfigDict
import pytest
from pathlib import Path
from whisper.settings import UserConfig


@pytest.fixture
def user_config(tmp_path):
    config_path = tmp_path / ".whisper"
    config_path.mkdir()
    config_file = config_path / "whisper.toml"
    config_file.write_text("""
    [default]
    copy_snippet = true
    config = "openai"
    theme = "solarized-dark"

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
    config_path = Path.home() / ".whisper" / "whisper.toml"
    assert config_path.read_text().find("new-api-key") != -1


def test_dot_notation_access(user_config):
    assert user_config.get_by_dot_notation("openai.api_key") == "test-api-key"
    user_config.set_by_dot_notation("openai.api_key", "updated-api-key")
    assert user_config.openai.api_key == "updated-api-key"
