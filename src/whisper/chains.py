from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .settings import UserConfig

config = UserConfig()


TEMPLATE = ChatPromptTemplate.from_template(
    """
You are an AI assistant that can answer questions and help with tasks.

{context}
"""
)


class CodeWhisper(BaseModel):
    language: str = Field(
        description="The programming language of the code snippet or terminal command"
    )
    description: str = Field(
        description="A description of the code snippet or terminal command"
    )
    snippet: str = Field(description="The code snippet or terminal command")


def create_chain(key: str = None, model: str = None):
    key = key or config.default
    model = model or getattr(config, key).model

    if key == "openai":
        return TEMPLATE | ChatOpenAI(
            model=model, temperature=0, openai_api_key=config.openai.api_key
        ).with_structured_output(CodeWhisper)
    elif key == "anthropic":
        return (
            TEMPLATE
            | ChatAnthropic(
                model=model, temperature=0, anthropic_api_key=config.anthropic.api_key
            )
            | StrOutputParser()
        )
    else:
        raise ValueError(f"Model {model} not found")
