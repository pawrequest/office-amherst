import shutil

import openpyxl
import pandas as pd

from assets.manager import AssetManagerContextOLD
from assets.entities import DFLT
from assets.identity import Identity


# from assets.manager import handle_id, check_progged

#
# def test_handle_id_with_valid_id():
#     # Valid ID '1111', expecting True
#     result = handle_id('1111', check_progged)
#     assert result is True
#
#
# #
# def test_handle_id_with_invalid_id():
#     # Invalid ID '2222', expecting False
#     result = handle_id('2222', check_progged)
#     assert result is False
#
#
# def test_handle_id_with_invalid_input():
#     # Invalid input type, expecting TypeError
#     with pytest.raises(ValueError):
#         handle_id(1234, check_progged)
#
#
# def test_handle_id_with_invalid_type():
#     # Invalid input type, expecting TypeError
#     with pytest.raises(TypeError):
#         handle_id(dict(), check_progged)
#


def test_top_three_rows():
    shutil.copy(DFLT.WB.value, DFLT.OUTPUT.value)
    in_rows = get_first_three_rows(DFLT.WB.value)
    out_rows = get_first_three_rows(DFLT.OUTPUT.value)
    assert in_rows == out_rows, f"Rows do not match: {in_rows} != {out_rows}"


def get_first_three_rows(filename):
    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    vals = [i for i in ws.values][0:3]
    return vals


def test_context_manager():
    with AssetManagerContextOLD(out_file=DFLT.OUTPUT.value) as am:
        df = am.df
    assert isinstance(df, pd.DataFrame)


def test_identity():
    with AssetManagerContextOLD(out_file=DFLT.OUTPUT.value) as am:
        # with AssetManagerContext(out_file=DFLT.OUTPUT.value) as am:
        radio = Identity(am.df, id_or_serial='1111')
        assert radio.id_number == '1111'
