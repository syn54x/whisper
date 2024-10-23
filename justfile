install:
    # Command to install dependencies
    echo "Installing dependencies..."
    uv sync
    pre-commit install

serve:
    # Command to serve the documentation
    echo "Serving documentation..."
    uv run mkdocs serve

lint:
    # Command to run linter
    echo "Running linter..."
    pre-commit run --all-files

test:
    uv run pytest -x

generate-gifs:
    echo "Generating gifs..."
    terminalizer render docs/assets/demo -o docs/assets/_demo.gif -q 50
    terminalizer render docs/assets/copy_a_snippet -o docs/assets/_copy_a_snippet.gif -q 50
    terminalizer render docs/assets/code_related_questions -o docs/assets/_code_related_questions.gif -q 50
    terminalizer render docs/assets/using_a_different_model -o docs/assets/_using_a_different_model.gif -q 50
    terminalizer render docs/assets/using_a_different_provider -o docs/assets/_using_a_different_provider.gif -q 50
    terminalizer render docs/assets/using_a_different_theme -o docs/assets/_using_a_different_theme.gif -q 50
    terminalizer render docs/assets/piping_content -o docs/assets/_piping_content.gif -q 50

    gifsicle -i docs/assets/_demo.gif -O3 --colors 256 --resize-width 600 --output docs/assets/demo.gif
    gifsicle -i docs/assets/_copy_a_snippet.gif -O3 --colors 256 --resize-width 600 --output docs/assets/copy_a_snippet.gif
    gifsicle -i docs/assets/_code_related_questions.gif -O3 --colors 256 --resize-width 600 --output docs/assets/code_related_questions.gif
    gifsicle -i docs/assets/_using_a_different_model.gif -O3 --colors 256 --resize-width 600 --output docs/assets/using_a_different_model.gif
    gifsicle -i docs/assets/_using_a_different_provider.gif -O3 --colors 256 --resize-width 600 --output docs/assets/using_a_different_provider.gif
    gifsicle -i docs/assets/_using_a_different_theme.gif -O3 --colors 256 --resize-width 600 --output docs/assets/using_a_different_theme.gif
    gifsicle -i docs/assets/_piping_content.gif -O3 --colors 256 --resize-width 600 --output docs/assets/piping_content.gif

    rm docs/assets/_*.gif
