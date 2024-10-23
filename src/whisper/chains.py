from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_fireworks import ChatFireworks
from langchain_mistralai import ChatMistralAI
from langchain_community.llms import GPT4All
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.pydantic import PydanticOutputParser

from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax


from .settings import UserConfig

config = UserConfig()


TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", "{system_prompt}"),
        ("user", "{context}"),
    ]
)


class CodeWhisper(BaseModel):
    is_prompt_code_related: bool = Field(
        default=False,
        description="Whether or not the prompt / question was code or command related",
    )
    title: str = Field(description="A short title for the AI's response")
    content: str = Field(
        description="The AI's response to the prompt in Markdown format."
    )
    language: str | None = Field(
        default=None,
        description="The programming language of the code snippet or terminal command",
    )
    snippet: str | None = Field(
        default=None,
        description="The code snippet or terminal command if the prompt was code related",
    )

    def render(self: "CodeWhisper", theme: str = "solarized-dark") -> Panel:
        return Panel(
            Markdown(self.content, code_theme=theme),
            title=self.title or "Result",
            border_style="green",
        )

    @staticmethod
    def render_syntax(
        syntax: Syntax,
        title: str,
        border_style: str = "green",
    ) -> Panel:
        return Panel(
            syntax,
            title=title,
            border_style=border_style,
        )


def create_chain(provider: str = None, model: str = None):
    provider = provider or config.default.provider
    model = model or getattr(config, provider).model

    if provider == "gpt4all":
        return TEMPLATE | GPT4All(model=model), PydanticOutputParser(
            pydantic_object=CodeWhisper
        )
    elif provider == "openai":
        return TEMPLATE | ChatOpenAI(
            model=model, temperature=0, openai_api_key=config.openai.api_key
        ).with_structured_output(CodeWhisper), None
    elif provider == "anthropic":
        return TEMPLATE | ChatAnthropic(
            model=model, temperature=0, anthropic_api_key=config.anthropic.api_key
        ).with_structured_output(CodeWhisper), None
    elif provider == "mistral":
        return TEMPLATE | ChatMistralAI(
            model=model, temperature=0, mistral_api_key=config.mistral.api_key
        ).with_structured_output(CodeWhisper), None
    elif provider == "fireworks":
        return TEMPLATE | ChatFireworks(
            model=model, temperature=0, fireworks_api_key=config.fireworks.api_key
        ).with_structured_output(CodeWhisper), None
    elif provider == "azureopenai":
        return TEMPLATE | AzureChatOpenAI(
            model=model, temperature=0, azure_api_key=config.azureopenai.api_key
        ).with_structured_output(CodeWhisper), None
    else:
        raise ValueError(f"Key {provider} not found")
