from inspect import isclass
import toml

from pathlib import Path
from typing import Type, Tuple

from pydantic_core import PydanticUndefinedType, ValidationError
from pydantic import BaseModel, Field
from rich.console import Console

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


class MistralAIConfig(BaseModelConfig):
    model: str = "pixtral-12b-2409"


class FireworksConfig(BaseModelConfig):
    model: str = "accounts/fireworks/models/llama-v3p1-405b-instruct"


class AzureOpenAIConfig(BaseModelConfig):
    model: str = "gpt-4o"


class DefaultConfig(BaseModel):
    copy_snippet: bool | None = None
    config: str = "openai"
    theme: str | None = "solarized-dark"


class UserConfig(BaseSettings):
    model_config = SettingsConfigDict(toml_file=["~/.whisper/whisper.toml"])

    default: DefaultConfig = Field(default_factory=DefaultConfig)

    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    anthropic: AnthropicConfig = Field(default_factory=AnthropicConfig)
    mistral: MistralAIConfig = Field(default_factory=MistralAIConfig)
    fireworks: FireworksConfig = Field(default_factory=FireworksConfig)
    azureopenai: AzureOpenAIConfig = Field(default_factory=AzureOpenAIConfig)

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
        path = Path(self.model_config["toml_file"][0])
        with path.open("w") as f:
            toml.dump(self.model_dump(), f)

    @classmethod
    def config_exists(cls):
        for path in cls.model_config["toml_file"]:
            if Path(path).exists():
                return True
        return False

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
    def initialize(
        cls,
        openai_key: str = None,
        anthropic_key: str = None,
        mistral_key: str = None,
        fireworks_key: str = None,
        azureopenai_key: str = None,
    ) -> str:
        def recurse_fields(cls_fields):
            data = {}
            for key, field in cls_fields.items():
                if isclass(field.annotation) and issubclass(
                    field.annotation, BaseModel
                ):
                    data[key] = recurse_fields(field.annotation.model_fields)
                elif not isinstance(field.default, PydanticUndefinedType):
                    data[key] = field.default
            return data

        config_data = recurse_fields(cls.model_fields)

        if openai_key is not None:
            config_data["openai"]["api_key"] = openai_key
        if anthropic_key is not None:
            config_data["anthropic"]["api_key"] = anthropic_key
        if mistral_key is not None:
            config_data["mistral"]["api_key"] = mistral_key
        if fireworks_key is not None:
            config_data["fireworks"]["api_key"] = fireworks_key
        if azureopenai_key is not None:
            config_data["azureopenai"]["api_key"] = azureopenai_key

        return toml.dumps(config_data)


try:
    config = UserConfig()
except ValidationError as e:
    console = Console()
    console.print(f"[red]Error: {e}[/red]")

    if not UserConfig.config_exists():
        console.print(
            "[yellow]No configuration file found.  Please run `whisper init` to initialize your configuration.[/yellow]"
        )
    else:
        console.print(
            "[yellow]It looks like your configuration file is malformed.  Please fix the errors and try again.[/yellow]"
        )
except Exception as e:
    console = Console()
    console.print(f"[red]Error: {e}[/red]")
