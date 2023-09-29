import numbers
import os
from typing import Union

import pandas as pd

pathy = Union[str, os.PathLike]


# def pd_is_numeric(col):
#     try:
#         pd.to_numeric(col)
#         return True
#     except:
#         return False
#
#
# def edit_ex_col(workbook: pathy, outfile: pathy, sheet_name: str, header_row_i: int, col_to_match: str,
#                 data_to_check: list, col_to_edit: str, data_to_insert):
#     skipped = []
#     df = pd.read_excel(workbook, sheet_name=sheet_name, header=header_row_i)
#     col_to_edit_type = df[col_to_edit].dtype
#     data_to_insert_type = type(data_to_insert)
#     if col_to_edit_type != data_to_insert_type:
#         if pd_is_numeric(df[col_to_edit]) and not isinstance(data_to_insert_type, numbers.Number):
#             if input(f"TypeMismatch : cast {col_to_edit} ({col_to_edit_type}) to {str(data_to_insert_type)}?") != 'y':
#                 print("Aborted.")
#                 exit()
#             df[col_to_edit] = df[col_to_edit].astype(data_to_insert_type)
#
#     if col_to_edit not in df.columns:
#         raise Exception(f"{col_to_edit=} not found in headers.")
#
#     for data in data_to_check:
#         matching_rows = df[df[col_to_match] == data]
#         if matching_rows.empty:
#             skipped.append(data)
#             continue
#
#         if len(matching_rows) > 1:
#             raise ValueError(f"Multiple rows found for {data}")
#
#         elif len(matching_rows) == 1:
#             index = matching_rows.index[0]
#             df.at[index, col_to_edit] = data_to_insert
#
#     if skipped:
#         if input(f"Missed_serials: {str(skipped)} \nContinue? (y/n): ") != 'y':
#             exit()
#
#     try:
#         df.to_excel(outfile, sheet_name=sheet_name, index=False)
#     except PermissionError as e:
#         print("Could not save file. Please close Excel and try again.")
#     except Exception as e:
#         print("An error occurred while saving the file: " + str(e))
#     else:
#         print("File saved successfully.")
#         return 0


def pd_is_numeric(col):
    try:
        pd.to_numeric(col)
        return True
    except:
        return False



def edit_ex_col(infile, outfile, sheet, header_i, col_match, data_match, col_edit, data_insert):
    df = pd.read_excel(infile, sheet_name=sheet, header=header_i)
    if pd_is_numeric(df[col_edit]) and not isinstance(data_insert, numbers.Number):
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
