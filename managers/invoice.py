import datetime
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd
from docx2pdf import convert as convert_word
from docxtpl import DocxTemplate

from entities.const import DFLT
from in_out.commence import cust_of_transaction
from managers.entities import Order
from entities.order import HireOrder

INVOICE_TMPLT = DFLT.INV_TMPLT


@dataclass
class Address1:
    add: str
    pc: str


@dataclass
class HireDates:
    invoice: datetime.date
    start: datetime.date
    end: datetime.date

    @classmethod
    def from_hire(cls, hire: pd.DataFrame):
        hire = hire.iloc[0]
        date_inv = hire['Booked Date']
        date_start = hire['Send Out Date']
        date_end = hire['Due Back Date']
        return cls(invoice=date_inv, start=date_start, end=date_end)


date_format = '%d.%m.%Y'


@dataclass
class SaleInvoice:
    inv_num: str
    dates: datetime.date
    inv_add: Address1
    del_add: Address1
    order: Order

    @classmethod
    def from_sale(cls, sale: pd.DataFrame, order: Order, customer: pd.Series, inv_num: Optional[str] = None):
        inv_num = inv_num or next_inv_num()
        del_add, inv_add = addresses_from_sale(sale)
        date_inv = sale['Invoice Date']
        return cls(inv_num=inv_num, dates=date_inv, inv_add=inv_add, del_add=del_add, order=order)


def addresses_from_sale(sale: pd.DataFrame) -> (Address1, Address1):
    sale = sale.iloc[0]
    i_add = sale['Invoice Address']
    i_pc = sale['Invoice Postcode']
    d_add = sale['Delivery Address']
    d_pc = sale['Delivery Postcode']
    inv_add = Address1(add=i_add, pc=i_pc)
    del_add = Address1(add=d_add, pc=d_pc)
    return del_add, inv_add


def addresses_from_hire_and_cust(customer, hire):
    customer, hire = customer.iloc[0], hire.iloc[0]
    i_add = customer['Address']
    i_pc = customer['Postcode']
    d_add = hire['Delivery Address']
    d_pc = hire['Delivery Postcode']
    inv_add = Address1(add=i_add, pc=i_pc)
    del_add = Address1(add=d_add, pc=d_pc)
    return del_add, inv_add


@dataclass
class HireInvoice(SaleInvoice):
    order: HireOrder
    dates: HireDates

    @classmethod
    def from_hire(cls, hire: pd.DataFrame, order: HireOrder, customer: pd.DataFrame = None,
                  inv_num: Optional[str] = None):
        assert len(hire) == 1
        hire = hire.iloc[0]

        customer = customer or cust_of_transaction(hire.Name, 'Hire')
        customer = customer.iloc[0]
        inv_num = inv_num or next_inv_num()

        del_add, inv_add = addresses_from_hire_and_cust(customer, hire)
        dates = HireDates.from_hire(hire)
        return cls(inv_num=inv_num, dates=dates, inv_add=inv_add, del_add=del_add, order=order)

    def generate(self, out_dir=None, open_file=False, prnt=False):
        doc = DocxTemplate(INVOICE_TMPLT)
        out_dir = out_dir or DFLT.GENERATED
        assert out_dir.is_dir()
        out_dir.mkdir(parents=True, exist_ok=True)  # This line creates the folder if it doesn't exist
        out_file = out_dir / f"{self.inv_num}.docx"
        self.order.shipping = format_currency(self.order.shipping)
        context = {
            'dates': self.dates,
            'inv_address': self.inv_add,
            'del_address': self.del_add,
            'order': self.order,
            'currency': format_currency,
            # 'self': self,
            'inv_num': self.inv_num,
        }
        try:
            doc.render(context)
            doc.save(out_file)

            pdf_convert(out_file)
            pdf_out_file = out_file.with_suffix('.pdf')

            if open_file:
                os.system(f'start {out_file}')
            if prnt:
                print_file(pdf_out_file)
        except Exception as e:
            ...


def pdf_convert(out_file: Path):
    try:
        convert_word(out_file, keep_active=True)
    except Exception as e:
        convert_libreoffice(docx_file=out_file)


def convert_libreoffice(docx_file: Path):
    out_dir = docx_file.parent
    subprocess.run(f'soffice --headless --convert-to pdf {str(docx_file)} --outdir {str(out_dir)}')


def format_currency(value):
    # return value
    # return f' £ {value:.2f}'
    if value == '':
        return ''
    return f"£{value:>8.2f}"


def print_file(file_path: Path):
    try:
        os.startfile(str(file_path), "print")
    except Exception as e:
        print(f"Failed to print: {e}")
        return False
    else:
        return True


def word_is_installed():
    try:
        os.startfile('winword.exe')
    except Exception as e:
        print(f"Failed to open Word: {e}")
        return False
    else:
        return True


def get_inv_nums(inv_dir) -> set[int]:
    inv_dir: Path = inv_dir if inv_dir.exists() else DFLT.INV_DIR_MOCK
    files = os.listdir(inv_dir)
    pattern = re.compile(r'^[Aa](\d{5}).*$')
    matching_files = [f.lower() for f in files if pattern.match(f)]
    inv_numbers = {int(pattern.match(f).group(1)) for f in matching_files}
    return inv_numbers

def next_inv_num(inv_dir=DFLT.INV_DIR):
    inv_dir: Path = inv_dir if inv_dir.exists() else DFLT.INV_DIR_MOCK
    print(f"Scanning invoices in {inv_dir}...")
    files = pd.Series(os.listdir(inv_dir)).sort_values(ascending=False)
    pattern = re.compile(r'^[Aa](\d{5}).*$')
    matching_files = files[files.str.match(pattern)]
    if len(matching_files) < 1:
        if DFLT.DEBUG:
            return 'A00000'
        else:
            raise FileNotFoundError(f"Not many invoice numbers found in {inv_dir}")

    highest = None
    for row in range(len(matching_files)):
        sub_series = matching_files.iloc[row:row + 10]
        # numerical_parts = sub_series.str.extract(pattern).astype(int)
        numerical_parts = sub_series.str.extract(pattern)[0]

        if numerical_parts.is_monotonic_decreasing:
            highest = sub_series.iloc[0]

    match = pattern.match(highest)
    if match:
        num = int(match.group(1))
        new_num = num + 1
        new_inv_num = f'A{new_num:05d}'
        return new_inv_num
    else:
        raise ValueError(f'Failed to parse invoice number from {highest}')


#
# # Usage
# new_inv_num = next_inv_num()
# print(new_inv_num)


# def get_inv_num(inv_dir=DFLT.INV_DIR):
#     inv_dir: Path = inv_dir if inv_dir.exists() else DFLT.INV_DIR_MOCK
#     print(f"Scanning invoices in {inv_dir}...")
#     files = pd.Series(os.listdir(inv_dir)).sort_values(ascending=False)
#     # pattern = re.compile(r'^[Aa](\d{5}).*$')
#     pattern = r'^[Aa](\d{5}).*$'
#     matching_files = files[files.str.match(pattern)]
#
#     for row in range(len(matching_files) - 10):
#         sub_series = matching_files.iloc[row:row + 10]
#         if sub_series.is_monotonic_decreasing:
#             highest = sub_series.iloc[0]
#             return highest
#
#     if DFLT.DEBUG:
#         if not matching_files.empty:
#             highest = matching_files.iloc[0]
#             return highest + 1
#         return 'A00000'
#
#     # Extract the numeric part, increment it, and format it back into the invoice number format
#     match = pattern.match(highest)
#     if match:
#         num = int(match.group(1))
#         new_num = num + 1
#         new_inv_num = f'A{new_num:05d}'
#         return new_inv_num
#     else:
#         raise ValueError(f'Failed to parse invoice number from {highest}')


