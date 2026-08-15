# curl -LsSf https://astral.sh/uv/install.sh | sh
# source $HOME/.local/bin/env
# uv sync --locked --all-extras
gunicorn --config gunicorn.py src.fastapi_adventures.app:app