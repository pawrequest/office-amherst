import os
import tempfile
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pytest
from openpyxl.reader.excel import load_workbook
from pandas import Series

from assets.manager import AssetManagerContext, DFLT, AssetManager
from in_out.excel import get_rows


def top_three_rows(in_wb, out_wb):
    in_rows = get_rows(in_wb)
    out_rows = get_rows(out_wb)
    assert in_rows == out_rows, f"Rows do not match: {in_rows} != {out_rows}"


@pytest.fixture
def am_fxt():
    with AssetManagerContext() as am:
        yield am


@pytest.fixture
def df_asset_fxt(am_fxt):
    asset: Series = am_fxt.row_from_serial_or_id('1111')
    yield asset


def test_am_context(am_fxt):
    fd, temp_filepath = tempfile.mkstemp(suffix='.xlsx')
    os.close(fd)
    temp_path = Path(temp_filepath)
    # df_overwrite_wb(DFLT.WB_AST.value, DFLT.SHEET.value, am_context.df_a, DFLT.HEAD.value, temp_path)
    # assert styles_match(DFLT.WB_AST.value, temp_path)
    excel_data = pd.read_excel(DFLT.WB_AST.value, sheet_name=DFLT.SHEET.value, header=DFLT.HEAD.value, dtype=str)
    df1 = am_fxt.df_a
    with AssetManagerContext(out_file=temp_path) as am2:
        df2 = am2.df_a
    assert df1.equals(df2)
    assert excel_data.equals(df2)
    assert styles_match(DFLT.WB_AST.value, temp_path)
    temp_path.unlink()


def styles_match(in_wb, out_wb) -> bool:
    in_styles = get_styles(in_wb)
    out_styles = get_styles(out_wb)
    return in_styles == out_styles


#
def get_styles(filename: Path, start=0, end=3):
    wb = load_workbook(filename)
    ws = wb.active
    styles = [[cell.style for cell in row] for row in ws.iter_rows(min_row=start + 1, max_row=end)]
    return styles


def test_id(df_asset_fxt):
    id_num = df_asset_fxt[DFLT.ID.value]
    assert id_num == '1111'


# def test_empty_serial(am_context_fxt):
#     radio = am_context_fxt.get_asset('3333')
#     assert radio.serial_number


def test_serial_num(am_fxt, df_asset_fxt):
    radio = am_fxt.row_from_serial_or_id('1111')
    assert radio[DFLT.SERIAL.value] == df_asset_fxt[DFLT.SERIAL.value]
    assert radio[DFLT.ID.value] == df_asset_fxt[DFLT.ID.value]


def test_df_asset_from_id(am_fxt, df_asset_fxt):
    radio = am_fxt.row_from_serial_or_id('1111')


def test_check_fw(am_fxt, df_asset_fxt):
    try:
        id_or = '1111'
        am_fxt.check_fw(id_or, fw_version='XXXX')
        am_fxt.check_fw(id_or)
    except Exception as e:
        raise e


def test_get_assets(am_fxt):
    nums = ['1111', '2222', '3333']
    assets = am_fxt.df_a.loc[am_fxt.df_a['Number'].isin(nums)]
    assert len(assets) == 3
    assert assets.iloc[1][DFLT.ID.value] == '2222'


def test_get_prices(am_fxt):
    price = am_fxt.get_sale_price('Hytera 405', 1)
    hire_price = am_fxt.get_hire_price('UHF', 1, 1)
    assert isinstance(price, Decimal)
    assert isinstance(hire_price, Decimal)


def test_smth(am_fxt, df_asset_fxt):
    radio = df_asset_fxt
    rad = am_fxt.row_from_serial_or_id('1111')
    am_fxt.set_field('1111', DFLT.FW.value, 'jjjjjjjj')
    assert am_fxt.get_field('1111', DFLT.FW.value) == 'jjjjjjjj'
    ...


# def test_from_row(am_fxt):
#     # row = am_fxt.row_from_serial_or_id('1111')
#     # res = am_fxt.get_field_from_row(row, 'FW')
#
#     ...

@pytest.fixture
def hire_item_fxt():
    return ('UHF', 10, 1)


# def test_line_item(am_fxt, hire_item_fxt):
#     product_name, qty, dur = hire_item_fxt
#     hire_price = am_fxt.get_hire_price(product_name, qty, dur)
#     line_item = HireLineItem(name=product_name, quantity=qty, duration=dur, price_each=hire_price)
#     ...

def test_make_hire_order(am_fxt:AssetManager):
    order_dict = {'UHF': 10}
    order_dict2 = {'UHF': 100}
    order = am_fxt.make_hire_order(order_dict, 1)
    order_price = order.total_price
    assert isinstance(order_price, Decimal)
    order2 = am_fxt.make_hire_order(order_dict, 3)
    order3 = am_fxt.make_hire_order(order_dict2, 3)
    order4 = am_fxt.make_hire_order(order_dict2, 4)
    assert order3.total_price >= order2.total_price >= order.total_price

    order_dict5 ={'Hytera 405' :5}
    order5 = am_fxt.make_sales_order(order_dict5)

    ...
