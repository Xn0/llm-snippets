from anthropic import Anthropic

from app.llm_config import PromptConfig
from app.logger import logger
from app.settings import settings
from .abc_llm import AbstractLLM


class AnthropicLLM(AbstractLLM, provider="anthropic"):

    @staticmethod
    def generate(prompt_config: PromptConfig, message: str) -> str:
        try:
            client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=prompt_config.model,
                max_tokens=prompt_config.max_tokens,
                system=prompt_config.system_prompt,
                temperature=prompt_config.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": message,
                    }
                ],
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic {e=}")
            return ""