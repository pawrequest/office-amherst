import pytest

from cmc.commence import CmcContext
from despatch.config import get_config_dict
from despatch.dbay_client import get_dbay_client
from office_tools.o_tool import OfficeTools


@pytest.fixture
def hire_from_cmc():
    with CmcContext() as cmc:
        yield cmc.hires_by_customer('Test')[0]


@pytest.fixture
def ot_auto():
    return OfficeTools.auto_select()





@pytest.fixture()
def dbay_client_sandbox(config_sandbox):
    return get_dbay_client(creds=config_sandbox.dbay_creds)


@pytest.fixture()
def dbay_client_production(config_production):
    return get_dbay_client(creds=config_production.dbay_creds)


@pytest.fixture()
def config_dict_from_toml():
    return get_config_dict(toml_file=MODEL_CONFIG_TOML)


@pytest.fixture()
def config_sandbox(config_dict_from_toml) -> Config:
    return config_from_dict(config_dict=config_dict_from_toml, sandbox=True)


def test_config_sandbox(config_sandbox):
    assert isinstance(config_sandbox, Config)
    assert config_sandbox.sandbox is True


@pytest.fixture()
def config_production(config_dict_from_toml) -> Config:
    return config_from_dict(config_dict=config_dict_from_toml, sandbox=False)


def test_config_prod(config_production):
    assert isinstance(config_production, Config)
    assert config_production.sandbox is False
