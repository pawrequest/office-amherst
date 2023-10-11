import os
import tempfile
from decimal import Decimal
from pathlib import Path

import pytest

from assets.manager import ManagerContext
from transactions.tran_manager import TransactionManager


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


def test_make_hire_order(tm_fxt):
    order_dict = {'UHF': 10}
    order_dict2 = {'UHF': 100}
    order = tm_fxt.make_hire_order(order_dict, 1)
    order_price = order.total_price
    assert isinstance(order_price, Decimal)
    order2 = tm_fxt.make_hire_order(order_dict, 3)
    order3 = tm_fxt.make_hire_order(order_dict2, 3)
    order4 = tm_fxt.make_hire_order(order_dict2, 4)
    assert order3.total_price >= order2.total_price >= order.total_price


def test_make_sale_order(tm_fxt):
    order_dict5 = {'Hytera 405': 5}
    order5 = tm_fxt.make_sales_order(order_dict5)
    assert isinstance(order5.total_price, Decimal)

    ...


def test_get_prices(tm_fxt):
    price = tm_fxt.get_sale_price('Hytera 405', 1)
    hire_price = tm_fxt.get_hire_price('UHF', 1, 1)
    assert isinstance(price, Decimal)
    assert isinstance(hire_price, Decimal)
    assert hire_price < price
