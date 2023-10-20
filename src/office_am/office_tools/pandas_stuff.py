import numbers

import pandas as pd


# def clean_empty_string_cols(df):
#     df2 = df.replace('', np.nan)
#     df2 = df2.replace(0, np.nan)
#     df2 = df2.replace('"', np.nan)
#     df2 = df2.replace("'", np.nan)
#
#     df2.dropna(axis=1, how='all')
#     return df2


# def get_col_dtype(col):
#     """
#     Infer datatype of a pandas column, process only if the column dtype is object.
#     input:   col: a pandas Series representing a df column.
#     """
#
#     if col.dtype == "object":
#         if 'Number ' in col:
#             return 'int'
#         if 'date' in col.name.lower():
#             new_col = pd.to_datetime(col, errors='raise', dayfirst=True)
#             return new_col
#
#         try:
#             col_new = pd.to_numeric(col.dropna(), errors='raise')
#             if col_new.astype(int).equals(col_new):  # Check if it's an integer
#                 return 'int'
#             else:
#                 return 'float'
#         except:
#             pass  # Continue to next check if not numeric
#
#         # Assume remaining object dtype columns are strings
#         return 'string'
#     else:
#         return col.dtype  # Return original dtype if not object dtype


# def parse_df(df: pd.DataFrame, dtype_map=None) -> pd.DataFrame:
#     row = df.iloc[0]
#     dtype_map = dtype_map or DTYPES.HIRE_PRICES
#
#     for col in df.columns:
#         if col in dtype_map:
#             df[col]:pd.DataFrame = df[col].astype(dtype_map[col])
#         else:
#             # d_emmp = clean_empty_string_cols(df)
#             # same2 = df.equals(d_emmp)
#             # df3 = types_from_values(df2)
#             df = types_from_cols(df)
#             ...
#     return df

# def types_from_cols(df:pd.DataFrame) -> pd.DataFrame:
#     for col in df.columns:
#         new_type = None
#         smth = df[col].dtype
#         if df[col].dtype != "object":
#             continue
#         elif 'number ' in col.lower():
#             new_type = 'int'
#
#         elif 'date' in col.lower():
#             try:
#                 date_obj = pd.to_datetime(df[col], errors='raise', dayfirst=True)
#             except:
#                 continue
#             else:
#                 new_type = date_obj.dtype
#
#         else:
#             try:
#                 number_obj = pd.to_numeric(col.dropna(), errors='raise')
#                 if number_obj.astype(int).equals(number_obj):
#                     new_type =  'int'
#                 else:
#                     new_type = 'float'
#
#             except:
#                 new_type = new_type or 'string'
#
#         df[col] = df[col].astype(new_type)
#     return df
#

# def types_from_values(df):
#     for col in df.columns:
#         for value in df.iloc[0]:
#             try:
#                 assert value.equals(int(value))
#                 df[col] = df[col].astype(int)
#             except:
#                 ...
#     return df


# def mapped_types(df, dtype_map):
#     # Filter the dtype_map to include only the columns that exist in df
#     valid_dtypes = {col: dtype for col, dtype in dtype_map.items() if col in df.columns}
#     return valid_dtypes

def df_is_numeric(col):
    try:
        pd.to_numeric(col)
        return True
    except:
        return False


def coerce_df_numtype(df: pd.DataFrame, col_header: str, data: str | int | float):
    if df_is_numeric(df[col_header]) and not isinstance(data, numbers.Number):
        ans = input(f"TypeMismatch : cast {col_header} ({df[col_header].dtype}) to {type(data)}? 's' to skip")
        if ans.lower() == 'y':
            df[col_header] = df[col_header].astype(type(data))
        elif ans == 's':
            return
        else:
            exit("Aborted.")
