import argparse
import shutil
from pathlib import Path

import PySimpleGUI as sg

from office_am.cmc.cmc_entities import CmcError
from office_am.cmc.commence import CmcContext
from office_am.dflt import DFLT_PATHS, DFLT_HIRE_EMAIL
from office_am.gui import invoice_gui
from office_am.merge_docs.merger import get_template_and_path
from office_am.office_tools.email_handler import EmailHandler, EmailError
from office_am.office_tools.file_management import print_file
from office_am.office_tools.o_tool import OfficeTools
from office_am.order.invoice import get_inv_temp
from office_am.order.transact import TransactionContext


# from .office_tools.email_handler import EmailError, EmailHandler
# from .office_tools.o_tool import OfficeTools
# from .gui import invoice_gui
# from .cmc.cmc_entities import CmcError
# from .cmc.commence import CmcContext
# from .dflt import DFLT_HIRE_EMAIL, DFLT_PATHS
# from .office_tools.file_management import print_file
# from .order.invoice import get_inv_temp
# from .order.transact import TransactionContext


def main(args):
    ot = OfficeTools.libre() if args.libre else OfficeTools.microsoft()

    with CmcContext() as cmc:
        hire = cmc.get_record_with_customer('Hire', args.hire_name)

        if args.box:
            do_boxes(hire)
            ...

        with TransactionContext() as tm:
            hire_inv = tm.get_hire_invoice(hire)
            out_file = (DFLT_PATHS.INV_OUT_DIR / hire_inv.inv_num).with_suffix('.docx')
            template, temp_file = get_inv_temp(hire_inv)

            if args.doall:
                do_all(cmc, temp_file, out_file, hire, ot)
            else:
                event_loop(cmc, temp_file, out_file, hire, ot)


def do_boxes(hire):
    boxes = hire['Boxes']
    for box in range(boxes):
        context = dict(
            date=f"{hire['Send Out Date']:%A %d %B}",
            method=hire['Send Method'],
            customer_name=hire['To Customer'],
            delivery_address=hire['Delivery Address'],
            delivery_contact=hire['Delivery Contact'],
            tel=hire['Delivery Tel'],
            packages=boxes,
        )
        template, temp_file = get_template_and_path(DFLT_PATHS.BOX_TMPLT, context=context)


def event_loop(cmc, temp_file, outfile, hire, ot: OfficeTools):
    window = invoice_gui()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Submit':
            if values['-SAVE-']:
                saved_docx = shutil.copy(temp_file, outfile)
                if not saved_docx:
                    raise FileNotFoundError(f'Failed to save {temp_file} to {outfile}')
                pdf_file = ot.pdf.from_docx(outfile)
                if values['-EMAIL-']:
                    do_email(pdf_file, ot.email)
                if values['-PRINT-']:
                    print_file(pdf_file)
                if values['-CMC-']:
                    do_cmc(cmc, 'Hire', hire, outfile)
            if values['-OPEN-']:
                opened = ot.doc.open_document(outfile if outfile.exists() else temp_file)
            break


def do_all(cmc, temp_file, outfile, hire, ot: OfficeTools):
    saved_docx = shutil.copy(temp_file, outfile)
    pdf_file = ot.pdf.from_docx(outfile)
    # print_file(outfile.with_suffix('.pdf'))
    do_cmc(cmc, 'Hire', hire, outfile)
    do_email(pdf_file, ot.email)
    opened = ot.doc.open_document(saved_docx or temp_file)

    ...


def do_cmc(cmc, table, transaction, outfile):
    package = {'Invoice': outfile}
    if 'test' not in transaction['Name'].lower():
        if sg.popup_ok_cancel(f'Log {transaction["Name"]} to CMC?') != 'OK':
            return
    try:
        cmc.edit_record(table, transaction['Name'], package)
    except CmcError as e:
        sg.popup_error(f"Failed to log to CMC with error: {e}")
    else:
        return True


def do_email(attachment: Path, handler: EmailHandler, email_=DFLT_HIRE_EMAIL):
    email_.attachment_path = attachment
    try:
        handler.send_email(email_)

    except EmailError as e:
        sg.popup_error(f"Email failed with error: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hire_name', help='The name of the hire')
    parser.add_argument('--print', action='store_true', help='Print the invoice after generating.')
    parser.add_argument('--openfile', action='store_true', help='Open the file.')
    parser.add_argument('--libre', action='store_true', help='Use Free Office tools.')
    parser.add_argument('--doall', action='store_true', help='save, convert to pdf, print, email, and log to commence.')
    parser.add_argument('--box', action='store_true', help='Send a box label')

    args = parser.parse_args()
    main(args)
