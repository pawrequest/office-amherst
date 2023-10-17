from pathlib import Path
from typing import Tuple

import PySimpleGUI as sg
from docxtpl import DocxTemplate

from entities.const import DFLT, format_currency
from entities.order import Address1, HireInvoice
from in_out.email_funcs import send_outlook
from in_out.file_management import pdf_convert, print_file


def get_inv_temp(inv_obj: HireInvoice, tmplt=DFLT.INV_TMPLT, temp_file=DFLT.TEMP_INV) -> Tuple[DocxTemplate, Path]:
    template = render_tmplt(inv_obj, tmplt, temp_file)
    return template, temp_file


def render_tmplt(inv_obj: HireInvoice, tmplt=DFLT.INV_TMPLT, temp_file=DFLT.TEMP_INV)->DocxTemplate:
    try:
        template = DocxTemplate(tmplt)
        context = invoice_template_context(inv_obj)
        template.render(context)
        template.save(temp_file)
        return template
    except Exception as e:
        raise e

def create_gui():
    layout = [
        [sg.Checkbox('Save', default=True, key='-SAVE-')],
        [sg.Checkbox('Print', default=False, key='-PRINT-')],
        [sg.Checkbox('Email', default=False, key='-EMAIL-')],
        [sg.Button('Submit')]
    ]
    window = sg.Window('Actions', layout)
    return window


def event_loop(word_doc, out_file):
    window = create_gui()
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Submit':

            if values['-SAVE-']:
                word_doc.SaveAs(str(out_file))
                word_doc.Close()
                pdf_convert(out_file)

            if values['-PRINT-']:
                print_file(out_file.with_suffix('.pdf'))

            if values['-EMAIL-']:
                send_outlook(out_file.with_suffix('.pdf'))
            break


def invoice_template_context(invoice):
    return {
        'dates': invoice.dates,
        'inv_address': invoice.inv_add,
        'del_address': invoice.del_add,
        'order': invoice.order,
        'currency': format_currency,
        # 'self': self,
        'inv_num': invoice.inv_num,
    }
