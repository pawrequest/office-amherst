import argparse

from managers import commence
from managers.invoice import HireInvoice
from managers.transact import TransactionContext


def main(args):
    with TransactionContext() as tm_in:
        tm = tm_in

    hire = commence.hire(args.hire_name)
    customer = commence.cust_of_transaction(hire.Name, 'Hire')
    hire_order = tm.make_hire_order(customer, hire)
    invoice = HireInvoice.from_hire(hire, hire_order, customer)
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
