from pathlib import Path

from dotenv import load_dotenv


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_env() -> None:
    root = project_root()
    candidates = [
        root / ".env",
        root.parent / ".env",
        root.parent.parent / ".env",
    ]
    for env_file in candidates:
        if env_file.exists():
            load_dotenv(env_file, override=True)
