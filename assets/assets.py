import logging
from pathlib import Path

import pandas as pd

from excel.excel import check_data, set_data




DFLT_INPUT_FILE = Path(__file__).resolve().with_name("assets_in.xls")
DFLT_OUTPUT_FILE = Path(__file__).resolve().with_name("assets_out.xls")
DFLT_SHEET_NAME = 'Sheet1'
DFLT_HEADER_ROW = 2

DFLT_BARCODE_HEADER = 'Barcode'
DFLT_ID_HEADER = 'Number'
DFLT_DATA_HEADER = 'REPROG'
DFLT_EXPECTED_VALUE = 'Y'


def get_excel(in_file=DFLT_INPUT_FILE, sheet=DFLT_SHEET_NAME, headers=DFLT_HEADER_ROW):
    return pd.read_excel(in_file, sheet_name=sheet, header=headers)


def get_function_to_call():
    while True:
        choice = input("Set or check? (s/c)").lower()
        if choice in ('s', 'c'):
            return set_progged if choice == 's' else check_progged
        print("Invalid option. Use 's' for set or 'c' for check.")


def handle_id(id_to_handle, action, df=None, barcode_header=DFLT_BARCODE_HEADER, id_header=DFLT_ID_HEADER,
              data_header=DFLT_DATA_HEADER, value=DFLT_EXPECTED_VALUE):
    if not isinstance(id_to_handle, (str, int)):
        raise TypeError("ID should be of type str or int")

    if df is None:
        df = get_excel()

    col_to_use = id_header if len(str(id_to_handle)) == 4 else barcode_header
    return action(df, id_to_handle, col_to_use, data_header, value)


def set_progged(df, id_to_handle, value_header, data_header, value, output_file=DFLT_OUTPUT_FILE):
    set_data(df, id_data=id_to_handle, id_header=value_header, value_header=data_header, value_data=value)
    df.to_excel(output_file, index=False)
    print("Excel sheet successfully updated.")
    return True


def set_fw_updated(df, id_data):
    set_data(df, id_data=id_data, id_header=value_header, value_header=data_header, value_data=value)

def check_progged(df, id_to_check, col_to_check, data_header, value):
    return check_data(df, id_data=id_to_check, id_header=col_to_check, value_header=data_header,
                      value_data=value)


def set_or_check():
    function_to_call = get_function_to_call()
    while True:
        id_to_handle = input("Enter ID\n")
        try:
            handle_id(id_to_handle, function_to_call)
        except ValueError:
            print(f"No or multiple results found for {id_to_handle}.")
        except PermissionError:
            print("Close Excel and retry.")
        except TypeError as e:
            print(e)


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='assets.log', level=logging.DEBUG)
        set_or_check()
    except Exception as e:
        logging.error(f"An error occurred: \n{e}")
        input("Press Enter to exit.")