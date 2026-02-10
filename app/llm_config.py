import dataclasses
import json
from importlib.resources import files
from pathlib import Path

from app.logger import logger
from app.settings import settings


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
        if conf_file.suffix != ".json":
            return
        try:
            _conf = json.loads(conf_file.read_bytes())
        except json.JSONDecodeError as e:
            logger.error(f"Config error, path={conf_file}, {e=}")
            return
        if conf_file.stem.startswith("_"):
            return
        print(conf_file.__dir__)
        cls._configs[conf_file.stem] = PromptConfig(**_conf)

    @classmethod
    def _init(cls) -> None:
        # default builtin configs
        for file in files("app.prompts").iterdir():
            if file.is_file():
                cls._load_conf(file)

        # custom overwrite configs
        if settings.PROMPT_CONFIGS_PATH.exists():
            for file in settings.PROMPT_CONFIGS_PATH.iterdir():
                if file.is_file():
                    cls._load_conf(file)

    @classmethod
    def get_config(cls, conf_name: str) -> PromptConfig | None:
        if conf_name not in cls._configs:
            logger.error(f"Config is missing {conf_name=}")
            return

        return cls._configs[conf_name]

    @classmethod
    def list_config_names(cls) -> list[str]:
        return list(cls._configs.keys())


def _get_config_repo():
    ConfigRepo._init()
    return ConfigRepo


config_repo = _get_config_repo
