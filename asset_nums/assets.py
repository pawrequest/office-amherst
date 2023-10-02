import pandas as pd

from excel.excel import check_data, set_data

# input_file = r'C:\paul\office_am\fixtures\asset_example.xls'
# sheet_name = 'Sheet1'
# header_row = 2
# output_file = r'C:\paul\office_am\fixtures\asset_example_out.xlsx'
#
# df = pd.read_excel(input_file, sheet_name=sheet_name, header=header_row)
#
# barcode_header = 'Barcode'
# id_header = 'Number'
# data_header = 'REPROG'
# expected_value = 'Y'

input_file = r'C:\paul\office_am\fixtures\asset_example.xls'
output_file = r'C:\paul\office_am\fixtures\asset_example_out.xlsx'
sheet_name = 'Sheet1'
header_row = 2

barcode_header = 'Barcode'
id_header = 'Number'
data_header = 'REPROG'
expected_value = 'Y'

# Read Excel file
df = pd.read_excel(input_file, sheet_name=sheet_name, header=header_row)

def get_excel(in_file = input_file, sheet=sheet_name, headers = header_row):
    return pd.read_excel(in_file, sheet_name=sheet, header=headers)
def get_function_to_call():
    while True:
        choice = input("Set or check? (s/c)").lower()
        if choice in ('s', 'c'):
            return set_progged if choice == 's' else check_progged
        print("Invalid option. Use 's' for set or 'c' for check.")


def set_progged(df: pd.DataFrame, id_to_handle: str | int, barcode_header: str = 'Barcode',
                id_header: str = 'Number', data_header: str = 'REPROG',
                value: str | int | float = 'Y'):
    col_to_set = id_header if len(id_to_handle) == 4 else barcode_header
    set_data(df, id_to_set=id_to_handle, col_to_set=col_to_set, data_header=data_header, value_to_set=value)
    df.to_excel(output_file, index=False)
    print("Excel sheet successfully updated.")


def check_progged(df: pd.DataFrame, id_to_handle: str | int, barcode_header: str = 'Barcode',
                  id_header: str = 'Number', data_header: str = 'REPROG',
                  value: str | int | float = 'Y'):
    col_to_check = id_header if len(id_to_handle) == 4 else barcode_header
    return check_data(df, id_to_check=id_to_handle, col_to_check=col_to_check, data_header=data_header,
                      expected_value=value)


def set_or_check():
    function_to_call = get_function_to_call()
    while True:
        id_to_handle = input("Enter ID\n")
        try:
            function_to_call(df, id_to_handle=id_to_handle, barcode_header=barcode_header,
                             id_header=id_header, value=expected_value)
        except ValueError:
            print(f"No or multiple results found for {id_to_handle}.")
        except PermissionError:
            print("Close Excel and retry.")


set_or_check()
