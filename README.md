![demo](https://github.com/user-attachments/assets/40130388-2452-4902-9bca-2fb76ad79ffe)

# `whisper` 🤫

## Install

To install Whisper, you can use pip:

```console
pip install just-whisper
```

## Setup

After installing Whisper, you need to initialize the configuration for Whisper. This involves setting up API keys for the services you intend to use, such as OpenAI or Anthropic.

To initialize the configuration, run:

```console
$ whisper init
```

This will create a basic configuration file in your home directory (`~/.whisper/whisper.toml`).  You should update this file with your API keys.

### Setup with keys

If you have keys for OpenAI or Anthropic handy, you can initialize the configuration with:

```console
$ whisper init --openai-key <your-openai-key> --anthropic-key <your-anthropic-key>
```

## Config

The whisper config file is located at `~/.whisper/whisper.toml`.  It looks like this:

```toml
# ~/.whisper/whisper.toml

default = "openai"

[openai]
api_key = "sk-proj-..."
model = "gpt-3.5-turbo"

[anthropic]
api_key = "sk-ant-..."
model = "claude-3-opus-20240229"
```

### Config Management

You can manage your config files using the `whisper config` command.  For example...

#### Show Config

```bash
❯ whisper config show
UserConfig(
│   default='openai',
│   openai=OpenAIConfig(api_key='replace-me', model='gpt-3.5-turbo'),
│   anthropic=AnthropicConfig(api_key='replace-me', model='claude-3-5-sonnet-20240620')
)
```

#### Get A Config Value

```bash
❯ whisper config get openai.model
gpt-3.5-turbo
```

#### Set A Config Value

```bash
❯ whisper config set openai.api_key "sk-proj-..."
UserConfig(
│   default='openai',
│   openai=OpenAIConfig(api_key='sk-proj-...', model='gpt-3.5-turbo'),
│   anthropic=AnthropicConfig(api_key='replace-me', model='claude-3-5-sonnet-20240620')
)
```
