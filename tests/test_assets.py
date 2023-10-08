import os
import shutil
import tempfile
from pathlib import Path

import pandas as pd
import pytest
from openpyxl.reader.excel import load_workbook

from assets.manager import AssetManager, AssetManagerContext, DFLT, Asset
from excel.excel import df_overwrite_wb, get_rows


@pytest.fixture
def dataframe_fxt():
    return pd.read_excel(DFLT.WB.value, sheet_name=DFLT.SHEET.value, header=DFLT.HEAD.value, dtype=str)


@pytest.fixture
def asset_manager_fxt(dataframe_fxt):
    return AssetManager(dataframe_fxt)


@pytest.fixture
def asset_fxt(asset_manager_fxt):
    return asset_manager_fxt.get_asset('1111')


def top_three_rows(in_wb, out_wb):
    in_rows = get_rows(in_wb)
    out_rows = get_rows(out_wb)
    assert in_rows == out_rows, f"Rows do not match: {in_rows} != {out_rows}"


@pytest.fixture
def temp_am_context(dataframe_fxt):
    fd, temp_filepath = tempfile.mkstemp(suffix='.xlsx')
    os.close(fd)
    temp_path = Path(temp_filepath)
    df_overwrite_wb(DFLT.WB.value, DFLT.SHEET.value, dataframe_fxt, DFLT.HEAD.value, temp_path)
    with AssetManagerContext(out_file=temp_path) as am:
        yield am, temp_path
    temp_path.unlink()

def test_context_manager2(temp_am_context, dataframe_fxt):
    am, temp_path = temp_am_context
    df = am.df
    assert df.equals(dataframe_fxt)
    df2 = pd.read_excel(temp_path, sheet_name=DFLT.SHEET.value, header=DFLT.HEAD.value, dtype=str)
    assert df.equals(df2)



def test_context_manager(dataframe_fxt):
    fd, temp_filepath = tempfile.mkstemp(suffix='.xlsx')
    os.close(fd)
    temp_path = Path(temp_filepath)
    try:
        df_overwrite_wb(DFLT.WB.value, DFLT.SHEET.value, dataframe_fxt, DFLT.HEAD.value, temp_path)
        with AssetManagerContext(out_file=temp_path) as am:
            df = am.df
        assert df.equals(dataframe_fxt)
        df2 = pd.read_excel(temp_path, sheet_name=DFLT.SHEET.value, header=DFLT.HEAD.value, dtype=str)
        assert df.equals(df2)
    finally:
        temp_path.unlink()
def get_styles(filename, start=0, end=3):
    wb = load_workbook(filename)
    ws = wb.active
    styles = [[cell.style for cell in row] for row in ws.iter_rows(min_row=start+1, max_row=end)]
    return styles

# def test_styles():
#     in_styles = get_styles(in_wb)
#     out_styles = get_styles(out_wb)
#     assert in_styles == out_styles, f"Styles do not match: {in_styles} != {out_styles}"


def test_id(asset_fxt):
    radio = asset_fxt
    assert radio.id_number == '1111'


def test_empty_serial(asset_manager_fxt):
    radio = asset_manager_fxt.get_asset('3333')
    assert radio.id_number == '3333'

def test_serial_num(asset_manager_fxt, asset_fxt):
    radio = asset_manager_fxt.get_asset(asset_fxt.serial_number)
    assert radio.id_number == asset_fxt.id_number

def test_check_fw(asset_manager_fxt, asset_fxt):
    assert asset_manager_fxt.check_progged(asset_fxt) is True


def test_get_aseets(asset_manager_fxt):
    nums = ['1111', '2222', '3333']
    assets = [asset_manager_fxt.get_asset(num) for num in nums]

def test_smth(asset_manager_fxt, asset_fxt):
    radio = asset_fxt
    rad = asset_manager_fxt.row_to_asset(0)
    rads = asset_manager_fxt.row_to_asset(0, 2)
    assert len(rads) == 2
    assert rads[0] == rad == radio
