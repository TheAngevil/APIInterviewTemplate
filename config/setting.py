import logging
from pathlib import Path
import yaml
import logging.config
from enum import Enum
from utils.file_handler import *


class EnumTestEnvironment(str, Enum):
    PROD = "PRODUCTION"
    STAGING = "STAGING"


class Settings:
    DEFAULT_API_VERSION = 'v1'
    # DEFAULT_SETTINGS_CONFIG = str(Path().cwd()/"config"/'setup.yml')
    DEFAULT_SETTINGS_CONFIG = str(Path().cwd().parent/"config"/'setup.yml')


    def _init_variables(self):
        self.url_prefix = self.setup_config[self.environment]["URL_PREFIX"]

    def __init__(self, request) -> None:
        # get custom config from command line args
        args = {
            'env': request.config.getoption('--env', default=None),
            'dataset': request.config.getoption('--dataset', default=None),
            'api_version': request.config.getoption('--api_version', default=None)
        }
        logging.info('input args: %s', args)

        with open(self.DEFAULT_SETTINGS_CONFIG, "r") as config:
            self.setup_config = yaml.load(config, Loader=yaml.FullLoader)

        self.set_env(args['env'])
        self.dataset = args["dataset"]
        self._init_variables()

    def set_env(self, env: str):
        self.environment = None
        for enum_env in EnumTestEnvironment:
            if env.upper() == enum_env.value:
                self.environment = env.upper()
                break
        if not self.environment:
            self.environment = EnumTestEnvironment.STAGING
        logging.info('testing env is set with: %s', self.environment)


