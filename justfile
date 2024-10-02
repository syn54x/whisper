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
