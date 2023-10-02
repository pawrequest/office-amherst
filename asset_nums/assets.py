from excel.excel import check_data, set_data
import pandas as pd


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



def get_function_to_call():
    while True:
        choice = input("Set or check? (s/c)").lower()
        if choice in ('s', 'c'):
            return set_progged if choice == 's' else check_progged
        print("Invalid option. Use 's' for set or 'c' for check.")

def set_progged(df: pd.DataFrame, id_to_handle: str | int, barcode_header: str, id_header: str, value_to_set: str | int | float):
    col_to_set = id_header if len(id_to_handle) == 4 else barcode_header
    set_data(df, id_to_set=id_to_handle, col_to_set=col_to_set, data_header=data_header, value_to_set=value_to_set)
    df.to_excel(output_file, index=False)
    print("Value set successfully.")

def check_progged(df: pd.DataFrame, id_to_handle: str | int, barcode_header: str, id_header: str, value_to_set: str | int | float = None):
    col_to_check = id_header if len(id_to_handle) == 4 else barcode_header
    return check_data(df, id_to_check=id_to_handle, col_to_check=col_to_check, data_header=data_header, expected_value=expected_value)

def set_or_check():
    function_to_call = get_function_to_call()

    while True:
        id_to_handle = input("Enter ID\n")
        try:
            function_to_call(df, id_to_handle=id_to_handle, barcode_header=barcode_header, id_header=id_header, value_to_set=expected_value)
        except ValueError as e:
            print(f"No or multiple results found for {id_to_handle}.")
        except PermissionError:
            print("Close Excel and retry.")

set_or_check()