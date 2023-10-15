import os
import re
import sys

# INV_FOLDER = r'C:\paul\scratch\inv'
INV_FOLDER = r'R:\ACCOUNTS\invoices'


def get_new_inv_num():
    inv_numbers = list(get_inv_nums())
    inv_numbers = sorted(inv_numbers, reverse=True)
    for index, num in enumerate(inv_numbers):
        if has_20_after(index=index, nums=inv_numbers):
            new_filename = f'A{num + 1}'
            return new_filename


def main_prompted():
    fn = get_new_inv_num()
    print(fn)
    input('Press Enter to close...')
    sys.exit(0)


def get_inv_nums() -> set[int]:
    inv_folder = INV_FOLDER
    files = os.listdir(inv_folder)
    pattern = re.compile(r'^[Aa](\d{5}).*$')
    matching_files = [f.lower() for f in files if pattern.match(f)]
    inv_numbers = {int(pattern.match(f).group(1)) for f in matching_files}
    return inv_numbers


def sequential_sublists(num_set: list):
    num_set = sorted(num_set)
    sequences = []
    current_sequence = [0]

    for num in num_set[1:]:
        if num == current_sequence[-1] + 1:
            current_sequence.append(num)
        else:
            if len(current_sequence) > 100:
                sequences.append(current_sequence)
            current_sequence = [num]

    return sequences


def has_20_after(index: int, nums: {int}):
    tally = 0
    while tally < 20:
        num = nums[index]
        next_num = nums[index + 1]
        if num == next_num + 1:
            tally += 1
            index += 1
        else:
            return False
    return True


if __name__ == '__main__':
    main_prompted()
