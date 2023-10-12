from pathlib import Path

from docx2pdf import convert

import datetime
import os
from dataclasses import dataclass
from decimal import Decimal

import pandas as pd
from docxtpl import DocxTemplate

from managers.entities import Order, DFLT, HireOrder
from managers.invoice_number import get_new_inv_num

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


date_format = '%d.%m.%Y'


@dataclass()
class HireInvoice:
    inv_num: str
    dates: HireDates
    inv_add: Address1
    del_add: Address1
    inv_order: Order
    ship_price: Decimal = 13

    @classmethod
    def from_hire(cls, hire: pd.Series, order: HireOrder, customer: pd.Series):
        inv_num = get_new_inv_num()
        i_add = customer['Address']
        i_pc = customer['Postcode']
        d_add = hire['Delivery Address']
        d_pc = hire['Delivery Postcode']
        inv_add = Address1(add=i_add, pc=i_pc)
        del_add = Address1(add=d_add, pc=d_pc)
        date_inv = hire['Booked Date']
        date_start = hire['Send Out Date']
        date_end = hire['Due Back Date']
        dates = HireDates(invoice=date_inv, start=date_start, end=date_end)
        return cls(inv_num=inv_num, dates=dates, inv_add=inv_add, del_add=del_add, inv_order=order)

    def generate(self, out_file=None, open=False, print=False):
        doc = DocxTemplate(INVOICE_TMPLT)
        out_file = DFLT.GENERATED / f"{self.inv_num + '.docx'}"



        context = {
            'currency': format_currency,
            'inv_num': self.inv_num,
            'dates': self.dates,
            'inv_address': self.inv_add,
            'del_address': self.del_add,
            'order': self.inv_order,
        }

        doc.render(context)
        doc.save(out_file)

        convert(out_file)  # This will save the PDF alongside the DOCX
        pdf_out_file = out_file.with_suffix('.pdf')

        if open:
            os.system(f'start {out_file}')
        if print:
            os.system(f'print {pdf_out_file}')

        # doc.close()


def format_currency(value):
    # return f' £ {value:.2f}'
    return f'£{value:>8.2f}'
