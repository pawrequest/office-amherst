import argparse
import asyncio

import PySimpleGUI as sg

from cmc import commence
from cmc.commence import hires_by_customer
from in_out.email_funcs import send_outlook
from in_out.file_management import LibreConverter, print_file
from managers.invoice import get_inv_temp
from managers.gui import create_gui
from managers.transact import TransactionContext
from entities.dflt import DFLT_EMAIL_O, DFLT_PATHS
from entities.office_tools import get_tools

DOC_HANDLER, EMAIL_SENDER, PDF_CONVERTER = get_tools()

def main(args):
    with TransactionContext() as tm:
        hire = commence.get_hire(args.hire_name)
        invoice = tm.hire_to_invoice(hire)
        invoice.generate(prnt=args.print, open_file=args.openfile)







def event_loop(res, outfile):
    window = create_gui()
    if res[1] is not None:
        process = res[0]
        doc = res[1]
    else:
        process = res[0]
        doc = outfile

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Submit':

            if values['-SAVE-']:
                DOC_HANDLER.save_document(doc)
                PDF_CONVERTER.convert(doc)

            if values['-PRINT-']:
                # print_file(doc.with_suffix('.pdf'))
                ...

            if values['-EMAIL-']:
                email_ = DFLT_EMAIL_O
                email_.attachment_path = doc.with_suffix('.pdf')
                EMAIL_SENDER.send_email(email_)

            break


def otherfunc():
    hires = hires_by_customer('Test')
    hire = hires[0]

    with TransactionContext() as tm:
        inv_obj = tm.hire_to_invoice(hire)


    template, temp_file = get_inv_temp(inv_obj)
    out_file = DFLT_PATHS.INV_OUT_DIR / f'{inv_obj.inv_num}.docx'
    opened = DOC_HANDLER.open_document(temp_file)
    saved = DOC_HANDLER.save_document(temp_file, out_file, keep_open=False)
    converted = PDF_CONVERTER.convert(out_file)
    # event_loop()


otherfunc()

#
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('hire_name', help='The name of the hire')
#     parser.add_argument('--print', action='store_true', help='Print the invoice after generating.')
#     parser.add_argument('--openfile', action='store_true', help='Open the file.')
#     parser.add_argument('--microsoft', action='store_true', help='Use Microsoft tools.')
#
#     args = parser.parse_args()
#     main(args)

