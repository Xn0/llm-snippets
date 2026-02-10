from abc import ABC, abstractmethod
from typing import Self

from app.llm_config import PromptConfig


class AbstractLLM(ABC):
    registry: dict[str, type[Self]] = {}

    def __init_subclass__(cls, *, provider: str, **kwargs):
        super().__init_subclass__(**kwargs)
        if provider in cls.registry:
            raise ValueError("Duplicate provider: {provider}")

        cls.registry[provider] = cls

    @staticmethod
    @abstractmethod
    def generate(prompt_config: PromptConfig, message: str) -> str:
        ...
