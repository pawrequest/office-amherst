import argparse
import os
from functools import partial

import pandas as pd

# def check_excel(workbook, data_to_check, col_with_name, sheet, col_with_data, header_i):
def check_excel(workbook, data_to_check, sheet,  col_with_name,  col_with_data, header_i):
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
        actual_status = row[col_with_data].iloc[0]
        print(f"Status for {data} is {actual_status}")
        input("Press enter to exit...")

check_paid = partial(check_excel,
                     col_with_name="No.",
                     sheet='Sales',
                     col_with_data='Status',
                     header_i=2
                     )


def main():
    parser = argparse.ArgumentParser(description='Check Excel file for data.')
    parser.add_argument('workbook', help='The Excel file to check')
    parser.add_argument('data_to_check', nargs='+', help='List of data to match')
    args = parser.parse_args()
    check_paid(workbook=args.workbook, data_to_check=args.data_to_check)



if __name__ == '__main__':
    main()
