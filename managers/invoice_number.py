import os
import re
import sys
from pathlib import Path

import pandas as pd

from managers.entities import DFLT

INV_FOLDER = Path(r'R:\ACCOUNTS\invoices')

#
# def get_new_inv_num() -> str | None:
#     try:
#         inv_numbers = list(get_inv_nums())
#     except FileNotFoundError:
#         return
#     inv_numbers = sorted(inv_numbers, reverse=True)
#     for index, num in enumerate(inv_numbers):
#         if has_20_after(index=index, nums=inv_numbers):
#             new_filename = f'A{num + 1}'
#             return new_filename

#
# def terminal_output():
#     inv_num = get_new_inv_num()
#     print(inv_num)
#     input('Press Enter to close...')
#     sys.exit(0)
#
#
# def get_inv_nums() -> set[int]:
#     inv_folder = INV_FOLDER
#     files = os.listdir(inv_folder)
#     pattern = re.compile(r'^[Aa](\d{5}).*$')
#     matching_files = [f.lower() for f in files if pattern.match(f)]
#     inv_numbers = {int(pattern.match(f).group(1)) for f in matching_files}
#     return inv_numbers


# def inv_nums_pd():
#     inv_folder:Path = INV_FOLDER if INV_FOLDER.is_dir() else DFLT.INV_DIR_MOCK
#     print(f"Scanning invoices in {inv_folder}...")
#     files = pd.Series(os.listdir(inv_folder)).sort_values(ascending=False)
#     pattern = re.compile(r'^[Aa](\d{5}).*$')
#     matching_files = files[files.str.match(pattern)]
#     for row in range (len(matching_files) -10 ):
#         sub_series = matching_files.iloc[row:row + 10]
#         if sub_series.is_monotonic_decreasing:
#             highest = sub_series.iloc[0]
#             return highest
#     else:
#         raise FileNotFoundError(f'No invoice numbers found in {inv_folder}')
#
#
#
# if __name__ == '__main__':
#     try:
#         inv_num1 = inv_nums_pd()
#     except FileNotFoundError:
#         print('No invoice numbers found')
#         inv_num1 = 'A00000'
#     ...
#
#     # terminal_output()
