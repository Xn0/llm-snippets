import dataclasses
import json
from importlib.resources import files
from pathlib import Path

from app.logger import logger
from app.settings import settings

BUILTIN_CONFIGS_PATH = ""

@dataclasses.dataclass
class PromptConfig:
    provider: str
    model: str
    temperature: float
    system_prompt: str
    max_tokens: int = 1024


class ConfigRepo:
    _configs: dict[str, PromptConfig] = {}

    @classmethod
    def _load_conf(cls, conf_file: Path) -> None:
        try:
            _conf = json.loads(conf_file.read_bytes())
        except json.JSONDecodeError as e:
            logger.error(f"Config error, path={conf_file}, {e=}")
            return

        cls._configs[conf_file.stem] = PromptConfig(**_conf)

    @classmethod
    def init(cls) -> None:
        # default builtin configs
        for conf in files("prompts").iterdir():
            cls._load_conf(conf)

        # custom overwrite configs
        if settings.PROMPT_CONFIGS_PATH.exists():
            for conf in settings.PROMPT_CONFIGS_PATH.iterdir():
                cls._load_conf(conf)

    @classmethod
    def get_config(cls, conf_name: str) -> PromptConfig | None:
        if conf_name not in cls._configs:
            logger.error(f"Config is missing {conf_name=}")
            return

        return cls._configs[conf_name]


def _get_config_repo():
    ConfigRepo.init()
    return ConfigRepo

config_repo = _get_config_repo