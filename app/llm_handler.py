from app.llm_config import config_repo
from app.llms import AbstractLLM
from app.logger import logger


class LLMHandler:
    @staticmethod
    def list_llm() -> list[str]:
        return list(AbstractLLM.registry.keys())

    @classmethod
    def _get_llm(cls, provider_name: str) -> AbstractLLM | None:
        if provider_name not in AbstractLLM.registry:
            logger.error(f"Unknown LLM {provider_name=}")
            return

        return AbstractLLM.registry[provider_name]

    @classmethod
    def run_request(cls, prompt_name: str, text: str) -> str | None:
        prompt_conf = config_repo().get_config(prompt_name)
        llm = cls._get_llm(prompt_conf.provider)
        return llm.generate(prompt_conf, text)
