import toml

from pathlib import Path
from typing import Type, Tuple

from pydantic_core import PydanticUndefinedType
from pydantic import BaseModel, Field

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class BaseModelConfig(BaseModel):
    api_key: str = "replace-me"
    model: str


class OpenAIConfig(BaseModelConfig):
    model: str = "gpt-3.5-turbo"


class AnthropicConfig(BaseModelConfig):
    model: str = "claude-3-5-sonnet-20240620"


class UserConfig(BaseSettings):
    model_config = SettingsConfigDict(toml_file=["~/.whisper/whisper.toml"])

    default: str = "openai"

    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    anthropic: AnthropicConfig = Field(default_factory=AnthropicConfig)

    def get_by_dot_notation(self, key: str):
        keys = key.split(".")
        value = self
        for k in keys:
            value = getattr(value, k)
        return value

    def set_by_dot_notation(self, key: str, value: str):
        keys = key.split(".")
        v = self
        for k in keys[:-1]:
            v = getattr(v, k)
        setattr(v, keys[-1], value)

    def save(self):
        path = Path.home() / ".whisper" / "whisper.toml"
        with path.open("w") as f:
            toml.dump(self.model_dump(), f)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)

    @classmethod
    def initialize(cls, openai_key: str = None, anthropic_key: str = None) -> str:
        def recurse_fields(cls_fields):
            data = {}
            for key, field in cls_fields.items():
                if issubclass(field.annotation, BaseModel):
                    data[key] = recurse_fields(field.annotation.model_fields)
                elif not isinstance(field.default, PydanticUndefinedType):
                    data[key] = field.default
            return data

        config_data = recurse_fields(cls.model_fields)

        if openai_key is not None:
            config_data["openai"]["api_key"] = openai_key
        if anthropic_key is not None:
            config_data["anthropic"]["api_key"] = anthropic_key

        return toml.dumps(config_data)
