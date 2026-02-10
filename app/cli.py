import click

from .logger import logger
from .llm_config import config_repo
from .llm_handler import LLMHandler

configs = config_repo().list_config_names()

@click.command()
@click.option('--command', type=str, required=True, help=f'Config name, options={" | ".join(configs)})')
@click.option('--text', type=str, required=True, help='text to pass to llm.')
def main(command, text):
    response = LLMHandler.run_request(command, text)
    logger.debug(response)
    print(response)


if __name__ == "__main__":
    main()
