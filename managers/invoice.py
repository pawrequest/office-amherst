import datetime
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from docx2pdf import convert as convert_word
from docxtpl import DocxTemplate
from win32com.client import Dispatch

from cmc.commence import get_customer
from entities.const import DFLT
from entities.order import HireOrder, Order
from managers.invoice_number import next_inv_num

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
    def from_hire(cls, hire: dict):
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
    def from_sale(cls, sale: dict, order: Order, inv_num: Optional[str] = None):
        inv_num = inv_num or next_inv_num()
        del_add, inv_add = addresses_from_sale(sale)
        date_inv = sale['Invoice Date']
        return cls(inv_num=inv_num, dates=date_inv, inv_add=inv_add, del_add=del_add, order=order)


def addresses_from_sale(sale: dict) -> (Address1, Address1):
    i_add = sale['Invoice Address']
    i_pc = sale['Invoice Postcode']
    d_add = sale['Delivery Address']
    d_pc = sale['Delivery Postcode']
    inv_add = Address1(add=i_add, pc=i_pc)
    del_add = Address1(add=d_add, pc=d_pc)
    return del_add, inv_add


def addresses_from_hire_and_cust(customer: dict, hire: dict):
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
    def from_hire(cls, hire: dict, order: HireOrder, inv_num: Optional[str] = None):

        customer = get_customer(hire['To Customer'])
        inv_num = inv_num or next_inv_num()

        del_add, inv_add = addresses_from_hire_and_cust(customer, hire)
        dates = HireDates.from_hire(hire)
        return cls(inv_num=inv_num, dates=dates, inv_add=inv_add, del_add=del_add, order=order)

    def generate(self, out_dir=None, open_file=False, prnt=False, email=True):
        doc = DocxTemplate(INVOICE_TMPLT)
        out_dir = out_dir or DFLT.INV_OUT_DIR
        assert out_dir.is_dir()
        # out_dir.mkdir(parents=True, exist_ok=True)  # This line creates the folder if it doesn't exist
        out_file = out_dir / f"{self.inv_num}.docx"
        # self.order.shipping = format_currency(self.order.shipping)
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
            if email:
                send_email(pdf_out_file)
        except Exception as e:
            raise e


def pdf_convert(out_file: Path):
    try:
        convert_word(out_file, keep_active=True)
    except Exception as e:
        convert_libreoffice(docx_file=out_file)
    finally:
        print(f"Converted {out_file}")


def convert_libreoffice(docx_file: Path):
    out_dir = docx_file.parent
    subprocess.run(f'soffice --headless --convert-to pdf {str(docx_file)} --outdir {str(out_dir)}')


def format_currency(value):
    # return value
    # return f' £ {value:.2f}'
    if value == '':
        return ''
    # if isinstance(value, str):
    #     value = Decimal(value)
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


def send_email(attachment_path):
    outlook = Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'admin@amherst.co.uk'  # replace with recipient's email
    mail.Subject = 'Invoice Attached'
    mail.Body = 'Please find the attached invoice.'
    mail.Attachments.Add(str(attachment_path))
    mail.Display(True)

    # To send the email uncomment the line below
    # mail.Send()
