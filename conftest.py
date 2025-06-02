import pytest
import logging
from datetime import datetime
from pathlib import Path
from config.setting import Settings

def pytest_addoption(parser):
    """
    adaptor of the command line variables
    :param parser:
    :return:
    """
    parser.addoption("--env", action='store', default = 'Staging',
                   choices=("staging", "Staging", "UAT", "uat", "dev", "Dev"), help="Testing Env, e.g.: Staging, UAT")
    parser.addoption('--dataset', action='store',
                     help='setup name of test data set (ex: test_data_set_1)')
    parser.addoption('--settings_file', action='store', default=None,
                     help='setup settings data located in project config directory as yaml')
    parser.addoption("--api_version", action="store", metavar="api_version", default=None,
                     help="only run tests matching the api version as api_version.")

@pytest.fixture(scope="session", autouse=True)
def setup(request):
    """
    sorting commands variables from request and default variables and package as Settings Class
    yield setup to
    :param request:
    :yield
    """
    setup = Settings(request)
    yield setup

def pytest_configure():
    """
    pytest_configure followed the known naming convention, and it is still called even without fixture decorated
    :return: None
    """
    project_path = Path.cwd()
    logs_dir = project_path / "logs"
    logs_dir.mkdir(exist_ok=True)

    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S %m-%d")
    log_file = logs_dir / f"{timestamp}.log"

    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, mode='w'),
            logging.StreamHandler()
        ]
    )


