import pytest

from cmc.commence import CmcContext
from office_tools.o_tool import OfficeTools


@pytest.fixture
def hire_from_cmc():
    with CmcContext() as cmc:
        yield cmc.hires_by_customer('Test')[0]


@pytest.fixture
def ot_auto():
    return OfficeTools.auto_select()
