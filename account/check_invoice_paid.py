import argparse
import os

import pandas as pd

from excel.excel import get_data_from_excel


def check_paid(df, id_data):
    return get_data_from_excel(df=df, id_header="No.", value_header="Status", id_data=id_data)


def main(args):
    if os.path.isfile(args.id_data):
        args.id_data = os.path.splitext(os.path.basename(args.id_data))[0]
    df = pd.read_excel(args.workbook, sheet_name='Sales', header=2)
    print(f"Checking {args.workbook} for {args.id_data}")
    result = check_paid(df=df, id_data=args.id_data)
    print(f"Value for {args.id_data} is {result}")
    input("Press enter to exit...")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check Excel file for data.')
    parser.add_argument('--workbook', help='The Excel file to check')
    parser.add_argument('--id_data', help='List of data to match')
    args = parser.parse_args()
    main(args)
