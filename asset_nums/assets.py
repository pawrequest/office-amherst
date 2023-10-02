from functools import partial

import pandas as pd

from excel.excel import check_data

excel_path = r'C:\paul\office_am\fixtures\asset_example.xls'
sheet_name = 'Sheet1'
header_row = 2

df = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_row)

# is_progged = partial(check_data, barcode_header='Barcode', id_header='Number', data_header='REPROG', expected_value='Y')


def is_progged(df: pd.DataFrame, id_to_check: str | int):
    return check_data(df, id_to_check, barcode_header='Barcode', id_header='Number', data_header='REPROG', expected_value='Y')

while True:
    id_to_check = str(input("Enter ID to check\n"))
    try:
        res = is_progged(df = df, id_to_check = id_to_check)
    except ValueError as e:
        print(e)
        continue
    print("yes" if res else "no")

