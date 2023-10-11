import os
import tempfile
from decimal import Decimal
from pathlib import Path

import pytest

from managers.asset_manager import AssetContext
from managers.cmc_manager import CommenceContext
from managers.tran_manager import TransactionManager, TransactionContext


@pytest.fixture
def commence_fxt():
    with CommenceContext() as cmc:
        yield cmc


@pytest.fixture
def tm_fxt() -> TransactionManager:
    with TransactionContext() as tm:
        yield tm


def test_get_prices(tm_fxt:TransactionManager):
    price = tm_fxt.get_sale_price('Hytera 405', 1)
    hire_price = tm_fxt.get_hire_price('UHF', 1, 1)
    assert isinstance(price, Decimal)
    assert isinstance(hire_price, Decimal)
    assert hire_price < price


def test_make_sale_order(commence_fxt, tm_fxt):
    sale = commence_fxt.customer_sales('Test').iloc[0]
    sale_order = tm_fxt.make_sale_order(sale)
    ...


def test_make_hire_order(commence_fxt, tm_fxt):
    hire = commence_fxt.customer_hires('Test').iloc[0]
    hire_order = tm_fxt.make_hire_order(hire, 1)
    ...
