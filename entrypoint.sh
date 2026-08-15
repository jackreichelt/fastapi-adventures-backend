curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --locked --all-extras
gunicorn --config gunicorn.conf.py src.fastapi_adventures.app:app