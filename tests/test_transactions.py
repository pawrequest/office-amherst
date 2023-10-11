import os
import tempfile
from decimal import Decimal
from pathlib import Path

import pytest

from assets.manager import ManagerContext
from in_out.cmc_direct import Commence
from transactions.tran_manager import TransactionManager


@pytest.fixture
def commence_fxt():
    cmc = Commence()
    yield cmc
@pytest.fixture
def manager_context_fxt():
    fd, out_file = tempfile.mkstemp(suffix='.xlsx')
    os.close(fd)
    out_file = Path(out_file)
    with ManagerContext(out_file=out_file) as context:
        yield context


@pytest.fixture
def tm_fxt(manager_context_fxt) -> TransactionManager:
    tm = manager_context_fxt[1]
    yield tm


@pytest.fixture
def hire_item_fxt():
    return ('UHF', 10, 1)


def test_make_sale_order(commence_fxt, tm_fxt):
    sale =  commence_fxt.customer_sales('Test').iloc[0]
    sale_order = tm_fxt.make_sales_order(sale)
    ...

def test_make_hire_order(commence_fxt, tm_fxt):
    hire = commence_fxt.customer_hires('Test').iloc[0]
    hire_order = tm_fxt.make_hire_order(hire, 1)
    ...


def test_get_prices(tm_fxt):
    price = tm_fxt.get_sale_price('Hytera 405', 1)
    hire_price = tm_fxt.get_hire_price('UHF', 1, 1)
    assert isinstance(price, Decimal)
    assert isinstance(hire_price, Decimal)
    assert hire_price < price
