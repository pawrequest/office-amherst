import argparse

import PySimpleGUI as sg

from cmc.cmc_entities import CmcError
from cmc.commence import CmcContext
from entities.dflt import DFLT_HIRE_EMAIL, DFLT_PATHS
from entities.office_tools import OfficeTools
from in_out.email_funcs import EmailError
from in_out.file_management import print_file
from managers.gui import create_gui
from managers.invoice import get_inv_temp
from managers.transact import TransactionContext


def main(args):
    ot = OfficeTools.libre() if args.libre else OfficeTools.microsoft()

    with CmcContext() as cmc:
        hire = cmc.get_hire(args.hire_name)
    with TransactionContext() as tm:
        hire_inv = tm.hire_to_invoice(hire)
    out_file = DFLT_PATHS.INV_OUT_DIR / f'{hire_inv.inv_num}.docx'
    template, temp_file = get_inv_temp(hire_inv)

    if args.doall:
        do_all(cmc, temp_file, out_file, hire, ot)
    else:
        event_loop(cmc, temp_file, out_file, hire, ot)


def event_loop(cmc, temp_file, outfile, hire, ot: OfficeTools):
    window = create_gui()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Submit':
            if values['-SAVE-']:
                saved = ot.doc.save_document(temp_file, outfile)
                converted = ot.pdf.from_docx(outfile)
                if values['-EMAIL-']:
                    do_email(converted, ot)
                if values['-PRINT-']:
                    print_file(converted)
                if values['-CMC-']:
                    do_cmc(cmc, hire, outfile)
            if values['-OPEN-']:
                opened = ot.doc.open_document(outfile)
            break



def do_all(cmc, temp_file, outfile, hire, ot: OfficeTools):
    opened = ot.doc.open_document(temp_file)
    doc = opened[1] or temp_file
    saved = ot.doc.save_document(doc, outfile)
    converted = ot.pdf.from_docx(outfile)
    # print_file(outfile.with_suffix('.pdf'))
    do_cmc(cmc, hire, outfile)

    # if 'test' not in hire['Name'].lower():
    #     if sg.popup_ok_cancel(f'Log {hire["Name"]} to CMC?') != 'OK':
    #         return
    # try:
    #     cmc.edit_hire(hire['Name'], package)
    # except CmcError as e:
    #     sg.popup_error(f"Failed to log to CMC with error: {e}")
    do_email(converted, ot)

    ...
def do_cmc(cmc, hire, outfile):
    package = {'Invoice': outfile}
    if 'test' not in hire['Name'].lower():
        if sg.popup_ok_cancel(f'Log {hire["Name"]} to CMC?') != 'OK':
            return
    try:
        cmc.edit_hire(hire['Name'], package)
    except CmcError as e:
        sg.popup_error(f"Failed to log to CMC with error: {e}")
    else:
        return True

def do_email(converted, ot):
    email_ = DFLT_HIRE_EMAIL
    email_.attachment_path = converted
    try:
        ot.email.send_email(email_)

    except EmailError as e:
        sg.popup_error(f"Email failed with error: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hire_name', help='The name of the hire')
    parser.add_argument('--print', action='store_true', help='Print the invoice after generating.')
    parser.add_argument('--openfile', action='store_true', help='Open the file.')
    parser.add_argument('--libre', action='store_true', help='Use Free Office tools.')
    parser.add_argument('--doall', action='store_true', help='save, convert to pdf, print, email, and log to commence.')

    args = parser.parse_args()
    main(args)
