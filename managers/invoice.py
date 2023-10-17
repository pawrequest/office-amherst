import PySimpleGUI as sg
import datetime
import os
from dataclasses import dataclass
from typing import Optional

from docxtpl import DocxTemplate
from win32com.client.gencache import EnsureDispatch

from cmc.commence import get_customer
from entities.const import DFLT, format_currency, invoice_template_context
from entities.order import HireOrder, Order
from in_out.file_management import pdf_convert, print_file, send_email
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
        try:
            doc = DocxTemplate(INVOICE_TMPLT)
            out_dir = out_dir or DFLT.INV_OUT_DIR
            out_file = out_dir / f"{self.inv_num}.docx"
            context = invoice_template_context(self)
            doc.render(context)


            temp_file = out_dir / '_temp_invoice.docx'

            event_loop(doc, out_file, temp_file)






            #
            # doc.save(out_file)
            #
            # pdf_convert(out_file)
            # pdf_out_file = out_file.with_suffix('.pdf')
            #
            #     print_file(pdf_out_file)
            # if email:
            #     send_email(pdf_out_file)
        except Exception as e:
            raise e


def open_word(doc_path):
    word = EnsureDispatch('Word.Application')
    word.Visible = True
    word_doc = word.Documents.Open(str(doc_path))
    return word, word_doc


def create_gui():
    layout = [
        [sg.Checkbox('Save', default=True, key='-SAVE-')],
        [sg.Checkbox('Print', default=False, key='-PRINT-')],
        [sg.Checkbox('Email', default=False, key='-EMAIL-')],
        [sg.Button('Submit')]
    ]
    window = sg.Window('Actions', layout)
    return window

def event_loop(doc, out_file, temp_file):
    doc.save(temp_file)
    os.system(f'start {temp_file}')

    window = create_gui()
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Submit':

            if values['-SAVE-']:
                doc.save(out_file)
                doc.close()
                pdf_convert(out_file)

            if values['-PRINT-']:
                print_file(out_file.with_suffix('.pdf'))

            if values['-EMAIL-']:
                send_email(out_file.with_suffix('.pdf'))
            break
