from pathlib import Path
from typing import Tuple

import PySimpleGUI as sg
from docxtpl import DocxTemplate

from entities.const import format_currency
from entities.order import HireInvoice
from src import DFLT_PATHS


def get_inv_temp(inv_obj: HireInvoice, tmplt=DFLT_PATHS.INV_TMPLT, temp_file=DFLT_PATHS.TEMP_INV) -> Tuple[
    DocxTemplate, Path]:
    template = render_tmplt(inv_obj, tmplt, temp_file)
    return template, temp_file


def render_tmplt(inv_obj: HireInvoice, tmplt=DFLT_PATHS.INV_TMPLT, temp_file=DFLT_PATHS.TEMP_INV) -> DocxTemplate:
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
