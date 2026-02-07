import dataclasses
import os
from pathlib import Path
from typing import Literal

import dotenv; dotenv.load_dotenv()


@dataclasses.dataclass(frozen=True)
class Settings:
    ENVIRONMENT: Literal["CLI"] = "CLI"  # TODO enum
    PROMPT_CONFIGS_PATH: Path = Path(
        os.environ.get("LLM_SNIPPETS_CONFIG_HOME", Path.home() / ".config" / "llm-snippets")
    )

    # API KEYS
    ANTHROPIC_API_KEY: str = dataclasses.field(default_factory=lambda : os.environ.get("ANTHROPIC_API_KEY", ""))

settings = Settings()