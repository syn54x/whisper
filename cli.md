# `whisper`

**Usage**:

```console
$ whisper [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `ask`: The default command that takes a prompt...
* `config`
* `init`: Initializes the configuration for Whisper,...
* `themes`: Prints a list of available syntax...

## `whisper ask`

The default command that takes a prompt and optional parameters to ask a question using Whisper.

**Usage**:

```console
$ whisper ask [OPTIONS] PROMPT
```

**Arguments**:

* `PROMPT`: The question you want to ask Whisper  [required]

**Options**:

* `-k, --key TEXT`: The API To use (openai, anthropic, etc)
* `-m, --model TEXT`: The model that Whisper should use
* `-t, --theme TEXT`: The theme that should be used for the output  [default: solarized-dark]
* `--help`: Show this message and exit.

## `whisper config`

**Usage**:

```console
$ whisper config [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Get the current configuration for Whisper.
* `set`: Initialize the configuration for Whisper.
* `show`: Show the current configuration for Whisper.

### `whisper config get`

Get the current configuration for Whisper.

**Usage**:

```console
$ whisper config get [OPTIONS] KEY
```

**Arguments**:

* `KEY`: The key to get the value for.  Supports dot notation.  e.g. 'openai.api_key'  [required]

**Options**:

* `--help`: Show this message and exit.

### `whisper config set`

Initialize the configuration for Whisper.

**Usage**:

```console
$ whisper config set [OPTIONS] KEY VALUE
```

**Arguments**:

* `KEY`: The key to set the value for.  Supports dot notation.  e.g. 'openai.api_key'  [required]
* `VALUE`: The value to set the key to.  [required]

**Options**:

* `--help`: Show this message and exit.

### `whisper config show`

Show the current configuration for Whisper.

**Usage**:

```console
$ whisper config show [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `whisper init`

Initializes the configuration for Whisper, saving API keys to a local file.

**Usage**:

```console
$ whisper init [OPTIONS]
```

**Options**:

* `--openai-key TEXT`: The OpenAI API key to use
* `--anthropic-key TEXT`: The Anthropic API key to use
* `--show / --no-show`: Show the configuration  [default: show]
* `--help`: Show this message and exit.

## `whisper themes`

Prints a list of available syntax highlighting themes from Pygments.

**Usage**:

```console
$ whisper themes [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
