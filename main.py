import argparse

from cmc import commence
from managers.invoice import HireInvoice
from managers.transact import TransactionContext


def main(args):
    with TransactionContext() as tm:
        hire = commence.get_hire(args.hire_name)
        invoice = tm.hire_to_invoice(hire)
        invoice.generate(prnt=args.print)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hire_name', help='The name of the hire')
    # parser.add_argument('--print', required=False)
    # parser.add_argument('--print', default='False', choices=['True', 'False'],
    #                     help='Print the invoice after generating.')
    parser.add_argument('--print', action='store_true', help='Print the invoice after generating.')

    args = parser.parse_args()
    main(args)
