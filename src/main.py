import argparse

import PySimpleGUI as sg

from cmc import commence
from cmc.cmc_entities import CmcError
from cmc.commence import edit_hire
from entities.dflt import DFLT_EMAIL_O, DFLT_PATHS
from entities.office_tools import OfficeTools
from in_out.email_funcs import EmailError
from managers.gui import create_gui
from managers.invoice import get_inv_temp
from managers.transact import TransactionContext


def main(args):
    ot = OfficeTools.get_tools(args.microsoft)
    hire = commence.get_hire(args.hire_name)
    with TransactionContext() as tm:
        hire_inv = tm.hire_to_invoice(hire)
    out_file = DFLT_PATHS.INV_OUT_DIR / f'{hire_inv.inv_num}.docx'
    template, temp_file = get_inv_temp(hire_inv)
    opened = ot.doc_handler.open_document(temp_file)

    if args.doall:
        do_all(temp_file, out_file, hire, ot)
    else:
        event_loop(temp_file, out_file, hire, opened, ot)


def event_loop(temp_file, outfile, hire, open_res, ot: OfficeTools):
    window = create_gui()
    doc = open_res[1] or outfile

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Submit':

            if values['-SAVE-']:
                saved = ot.doc_handler.save_document(doc, outfile, keep_open=False)
                converted = ot.pdf_converter.from_docx(outfile)
                # always save if emailing
                if values['-EMAIL-']:
                    email_ = DFLT_EMAIL_O
                    email_.attachment_path = converted
                    ot.email_sender.send_email(email_)
            if values['-PRINT-']:
                # print_file(doc.with_suffix('.pdf'))
                ...
            if values['-CMC-']:
                package = {'Invoice': outfile}
                edit_hire(hire['Name'], package)
                ...
            break


def do_all(temp_file, outfile, hire, ot: OfficeTools):
    sg.popup_quick_message('Saving...')
    saved = ot.doc_handler.save_document(temp_file, outfile, keep_open=False)
    sg.popup_quick_message('Converting...')
    converted = ot.pdf_converter.from_docx(outfile)
    sg.popup_quick_message('Emailing...')
    email_ = DFLT_EMAIL_O
    email_.attachment_path = converted
    try:
        ot.email_sender.send_email(email_)
    except EmailError as e:
        sg.popup_error(f"Email failed with error: {e}")

    sg.popup_quick_message('Printing...')
    # print_file(doc.with_suffix('.pdf'))
    sg.popup_quick_message('Logging to CMC...')
    package = {'Invoice': outfile}
    try:
        edit_hire(hire['Name'], package)
    except CmcError as e:
        sg.popup_error(f"Failed to log to CMC with error: {e}")
    sg.popup_ok('Done!')

    ...


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hire_name', help='The name of the hire')
    parser.add_argument('--print', action='store_true', help='Print the invoice after generating.')
    parser.add_argument('--openfile', action='store_true', help='Open the file.')
    parser.add_argument('--microsoft', action='store_true', help='Use Microsoft tools.')
    parser.add_argument('--doall', action='store_true', help='save, convert to pdf, print, email, and log to commence.')

    args = parser.parse_args()
    main(args)
