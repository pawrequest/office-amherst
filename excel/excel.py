import numbers
import os
from typing import Union

import pandas as pd

pathy = Union[str, os.PathLike]


def df_is_numeric(col):
    try:
        pd.to_numeric(col)
        return True
    except:
        return False


def edit_excel(infile: pathy, outfile: pathy, sheet: str, header_i: int, col_match: str, data_match: str, col_edit: str,
               data_insert: str):
    df = pd.read_excel(infile, sheet_name=sheet, header=header_i)
    if df_is_numeric(df[col_edit]) and not isinstance(data_insert, numbers.Number):
        if input(f"TypeMismatch : cast {col_edit} ({df[col_edit].dtype}) to {type(data_insert)}?") != 'y':
            exit("Aborted.")
        df[col_edit] = df[col_edit].astype(type(data_insert))

    if col_edit not in df.columns: raise Exception(f"{col_edit} not found.")

    skipped = []
    for data in data_match:
        rows = df[df[col_match] == data]
        if rows.empty: skipped.append(data); continue
        if len(rows) != 1: raise ValueError(f"Multiple rows for {data}")
        df.at[rows.index[0], col_edit] = data_insert

    if skipped and input(f"Missed: {skipped}\nContinue?") != 'y': exit()

    try:
        df.to_excel(outfile, sheet_name=sheet, index=False)
    except PermissionError:
        print("Close Excel and retry.")
    except Exception as e:
        print(f"Error: {e}")
    else:
        print("Saved.")
        return 0


def check_excel(workbook: pathy, data_to_check: str, sheet: str, col_with_name: str, col_with_data: str, header_i: int):
    if isinstance(data_to_check, str):
        data_to_check = [data_to_check]
    for i, in_data in enumerate(data_to_check):
        if os.path.isfile(in_data):
            data_to_check[i] = os.path.splitext(os.path.basename(in_data))[0]

    print(f"Checking {workbook} for {data_to_check}")
    df = pd.read_excel(workbook, sheet_name=sheet, header=header_i)

    for data in data_to_check:
        row = df[df[col_with_name].str.upper() == data.upper()]
        if len(row) != 1:
            print(f"No or multiple results found for {data}")
            input("Press enter to continue...")
            continue
        actual_data = row[col_with_data].iloc[0]
        print(f"Value for {data} is {actual_data}")
        input("Press enter to exit...")


def check_excel_file2(df: pd.DataFrame, target_data, name_col, data_col):
    # Convert single string to list for uniform handling
    target_data = [target_data] if isinstance(target_data, str) else target_data

    for data in target_data:
        row = df[df[name_col].str.upper() == data.upper()]

        if len(row) != 1:
            input(f"No or multiple results found for {data} - Press enter to continue to next value.")
            continue

        actual_data = row[data_col].iloc[0]
        print(f"Value for {data} is {actual_data}")

    input("Press enter to exit...")


def is_progged(df: pd.DataFrame, id_to_check: str | int, barcode_header: str, id_header: str, reprogged_header: str,
               reprogged_tag: str):
    col_to_check = id_header if len(str(id_to_check)) == 4 else barcode_header
    row = df[df[col_to_check].astype(str) == str:id_to_check]
    if len(row) != 1:
        raise ValueError(f"No or multiple results found for {id}")
    return reprogged_tag == row[reprogged_header].iloc[0]

def check_data(df: pd.DataFrame, id_to_check: Union[str, int], barcode_header: str, id_header: str,
               data_header: str, expected_value: Union[str, int, float]) -> bool:

    col_to_check = id_header if len(str(id_to_check)) == 4 else barcode_header
    row = df[df[col_to_check].astype(str) == str(id_to_check)]
    if len(row) != 1:
        raise ValueError(f"No or multiple results found for {id_to_check}")
    return expected_value == row[data_header].iloc[0]