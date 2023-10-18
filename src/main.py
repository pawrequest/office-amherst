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
from entities.dflt import DFLT_EMAIL_O, get_tools, DFLT_PATHS

DOC_HANDLER, EMAIL_SENDER, PDF_CONVERTER = get_tools()

async def main(args):
    with TransactionContext() as tm:
        hire = commence.get_hire(args.hire_name)
        invoice = tm.hire_to_invoice(hire)
        invoice.generate(prnt=args.print, open_file=args.openfile)


async def wait_for_process(process):
    while True:
        res = process.poll()
        if res is not None:
            break
        await asyncio.sleep(3)
    print("Process has finished.")


async def otherfunc():
    hires = hires_by_customer('Test')
    hire = hires[0]


    with TransactionContext() as tm:
        inv_obj = tm.hire_to_invoice(hire)


    template, temp_file = get_inv_temp(inv_obj)
    process = DOC_HANDLER.open_document(temp_file)[0]
    wait_task = asyncio.create_task(wait_for_process(process))

    avar = event_loop( temp_file, DFLT_PATHS.INV_OUT_DIR / 'test_invoice.docx')




    await wait_task


otherfunc()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hire_name', help='The name of the hire')
    parser.add_argument('--print', action='store_true', help='Print the invoice after generating.')
    parser.add_argument('--openfile', action='store_true', help='Open the file.')
    parser.add_argument('--microsoft', action='store_true', help='Use Microsoft tools.')

    args = parser.parse_args()
    main(args)


def event_loop(word_doc, out_file):
    window = create_gui()
    opened_doc = DOC_HANDLER.open_document(out_file)[0]
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Submit':

            if values['-SAVE-']:
                word_doc.SaveAs(str(out_file))
                word_doc.Close()
                PDF_CONVERTER.convert(out_file)

            if values['-PRINT-']:
                print_file(out_file.with_suffix('.pdf'))

            if values['-EMAIL-']:
                email_ = DFLT_EMAIL_O
                email_.attachment_path = out_file.with_suffix('.pdf')
                EMAIL_SENDER.send_email(email_)

            break
