activate:
    # Command to activate the environment
    echo "Activating environment..."
    source .venv/bin/activate

install:
    # Command to install dependencies
    echo "Installing dependencies..."
    rye sync
    pre-commit install

lint:
    # Command to run linter
    echo "Running linter..."
    pre-commit run --all-files
