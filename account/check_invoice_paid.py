import argparse
from functools import partial

from excel.excel import check_excel

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
