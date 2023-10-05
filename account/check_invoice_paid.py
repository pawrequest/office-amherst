import argparse
import os

import pandas as pd


# check_paid = partial(check_data,
#                      col_with_name="No.",
#                      sheet='Sales',
#                      col_with_data='Status',
#                      header_i=2
#                      )



# def check_excel(workbook: pathy, data_to_check: str, sheet: str, col_with_name: str, col_with_data: str, header_i: int):
#     if isinstance(data_to_check, str):
#         data_to_check = [data_to_check]
#     for i, in_data in enumerate(data_to_check):
#         if os.path.isfile(in_data):
#             data_to_check[i] = os.path.splitext(os.path.basename(in_data))[0]
#
#     print(f"Checking {workbook} for {data_to_check}")
#     df = pd.read_excel(workbook, sheet_name=sheet, header=header_i)
#
#     for data in data_to_check:
#         row = df[df[col_with_name].str.upper() == data.upper()]
#         if len(row) != 1:
#             print(f"No or multiple results found for {data}")
#             input("Press enter to continue...")
#             continue
#         actual_data = row[col_with_data].iloc[0]
#         print(f"Value for {data} is {actual_data}")
#         input("Press enter to exit...")
#


def get_data_from_excel(df:pd.DataFrame, id_data: str, id_header: str, value_header: str):
    """ Returns True if value_data is in col value_header for row id_data.
    :param df: DataFrame to search
    :param id_data: Data to search for
    :param id_header: Header for id of record to search
    :param value_header: Column name for data to return
    """
    row = df[df[id_header].str.upper() == id_data.upper()]
    if len(row) != 1:
        print(f"No or multiple results found for {id_data}")
        input("Press enter to continue...")
    actual_data = row[value_header].iloc[0]
    return actual_data


def check_paid(df, id_data):
    return get_data_from_excel(df=df, id_header="No.", value_header="Status", id_data=id_data)


def main(args):
    if os.path.isfile(args.id_data):
        args.id_data = os.path.splitext(os.path.basename(args.id_data))[0]
    df = pd.read_excel(args.workbook, sheet_name='Sales', header=2)
    print (f"Checking {args.workbook} for {args.id_data}")
    result = check_paid(df=df, id_data=args.id_data)
    print(f"Value for {args.id_data} is {result}")
    input("Press enter to exit...")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check Excel file for data.')
    parser.add_argument('--workbook', help='The Excel file to check')
    parser.add_argument('--id_data', help='List of data to match')
    args = parser.parse_args()
    main(args)

