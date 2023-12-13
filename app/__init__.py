from pathlib import Path

import tomllib

with Path.open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
    version = data["tool"]["poetry"]["version"]
