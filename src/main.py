import argparse
import PySimpleGUI as sg
from cmc import commence
from cmc.commence import hires_by_customer
from entities.const import DFLT
from in_out.email_funcs import GmailSender, OutlookSender
from in_out.file_management import LibreConverter, LibreOpener, WordOpener
from managers.invoice import create_gui, get_inv_temp
from managers.transact import TransactionContext

from src import DFLT_EMAIL_O
def main(args):
    with TransactionContext() as tm:
        hire = commence.get_hire(args.hire_name)
        invoice = tm.hire_to_invoice(hire)
        invoice.generate(prnt=args.print, open_file=args.openfile)


def otherfunc():
    # many = lots_of_hires()
    # customrs = get_customer('Test')
    hires = hires_by_customer('Test')
    hire = hires[0]

    # doc_handler = WordOpener()
    # email_sender = OutlookSender()
    doc_handler = LibreOpener()
    email_sender = GmailSender()

    with TransactionContext() as tm:
        inv_obj = tm.hire_to_invoice(hire)
    template, temp_file = get_inv_temp(inv_obj)
    doc_handler.open_document(temp_file)


    pdf_converter = LibreConverter()
    pdf_converter.convert(temp_file.with_suffix('.pdf'))


    email_ = DFLT_EMAIL_O
    email_.attachment_path = temp_file.with_suffix('.pdf')
    email_sender.send_email(email_)


otherfunc()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hire_name', help='The name of the hire')
    parser.add_argument('--print', action='store_true', help='Print the invoice after generating.')
    parser.add_argument('--openfile', action='store_true', help='Open the file.')

    args = parser.parse_args()
    main(args)


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
