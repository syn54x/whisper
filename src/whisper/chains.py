from pydantic import BaseModel, Field, field_validator, ValidationInfo
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from rich.panel import Panel
from rich.markdown import Markdown

from .settings import UserConfig

config = UserConfig()


TEMPLATE = ChatPromptTemplate.from_template(
    """
You are an AI assistant that can answer questions and help with tasks.

{context}
"""
)


class CodeWhisper(BaseModel):
    is_prompt_code_related: bool = Field(
        description="Whether or not the prompt / question was code or command related"
    )
    title: str = Field(description="A short title for the AI's response")
    content: str = Field(
        description="The AI's response to the prompt in Markdown format."
    )
    language: str | None = Field(
        description="The programming language of the code snippet or terminal command"
    )
    snippet: str | None = Field(
        description="The code snippet or terminal command if the prompt was code related"
    )

    @field_validator("language", "snippet", mode="before")
    @classmethod
    def check_code_related_fields(cls, v: str, info: ValidationInfo):
        if info.data.get("is_prompt_code_related") and not v:
            raise ValueError(
                f"The [{info.field_name}] must be provided if the prompt was code related"
            )
        return v

    def render(self: "CodeWhisper", theme: str = "solarized-dark") -> Panel:
        return Panel(
            Markdown(self.content, code_theme=theme),
            title=self.title or "Result",
            border_style="green",
        )


class ChainFactory:
    def __init__(self, key: str = None, model: str = None):
        self.config = UserConfig()

    def create(self, key: str = None, model: str = None):
        key = key or self.config.default
        model = model or getattr(self.config, key).model

        pass


def create_chain(key: str = None, model: str = None):
    key = key or config.default
    model = model or getattr(config, key).model

    if key == "openai":
        return TEMPLATE | ChatOpenAI(
            model=model, temperature=0, openai_api_key=config.openai.api_key
        ).with_structured_output(CodeWhisper)
    elif key == "anthropic":
        return TEMPLATE | ChatAnthropic(
            model=model, temperature=0, anthropic_api_key=config.anthropic.api_key
        ).with_structured_output(CodeWhisper)
    else:
        raise ValueError(f"Model {model} not found")
