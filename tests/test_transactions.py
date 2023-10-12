import os
import tempfile
from decimal import Decimal
from pathlib import Path

import pytest
import win32com.client

from managers.asset_manager import AssetContext
from managers.tran_manager import TransactionManager, TransactionContext
from managers import cmc_manager

@pytest.fixture
def commence_fxt():
    yield win32com.client.Dispatch(f"Commence.DB")
@pytest.fixture
def hire_cursor_fxt(commence_fxt):
    cursor = commence_fxt.GetCursor(0, 'Hire', 0)
    yield cursor

@pytest.fixture
def sale_cursor_fxt(commence_fxt):
    cursor = commence_fxt.GetCursor(0, 'Sale', 0)
    yield cursor

@pytest.fixture
def customer_cursor_fxt(commence_fxt):
    cursor = commence_fxt.GetCursor(0, 'Customer', 0)
    yield cursor

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


# def test_make_sale_order(tm_fxt, sale_cursor_fxt):
#     sales = cmc_manager.sales_by_customer('Test')
#     sale = sales.iloc[0]
#     sale_order = tm_fxt.make_sale_order(sale)
#     ...


def test_make_hire_order(hire_cursor_fxt, tm_fxt):
    hires = cmc_manager.hires_by_customer('Test')
    hire = hires.iloc[0]
    hire_order = tm_fxt.make_hire_order(hire, 1)
    ...
