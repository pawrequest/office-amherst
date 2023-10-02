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


# def check_data(df: pd.DataFrame, id_to_check: Union[str, int], col_to_check:str,
#                data_header: str, expected_value: Union[str, int, float]) -> bool:
#
#     row = df[df[col_to_check].astype(str) == str(id_to_check)]
#     if len(row) != 1:
#         raise ValueError(f"No or multiple results found for {id_to_check}")
#     return expected_value == row[data_header].iloc[0]
#
# def set_data(df: pd.DataFrame, id_to_set: str | int, col_to_set: str, data_header: str, value_to_set: str | int | float):
#     index_to_set = df[df[col_to_set].astype(str) == str(id_to_set)].index
#     if len(index_to_set) != 1:
#         raise ValueError(f"No or multiple results found for {id_to_set}")
#     df.at[index_to_set[0], data_header] = value_to_set
#
#     return True



def check_data(df: pd.DataFrame, id_to_check: str | int, col_to_check:str, data_header: str, expected_value: str | int | float) -> bool:
    row = df[df[col_to_check].astype(str) == str(id_to_check)]
    if len(row) != 1:
        raise ValueError()
    res = expected_value == row[data_header].iloc[0]
    print('yes' if res else 'no')
    return res

def set_data(df: pd.DataFrame, id_to_set: str | int, col_to_set: str, data_header: str, value_to_set: str | int | float):
    index_to_set = df[df[col_to_set].astype(str) == str(id_to_set)].index
    if len(index_to_set) != 1:
        raise ValueError()
    df.at[index_to_set[0], data_header] = value_to_set
    return True