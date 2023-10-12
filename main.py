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
    invoice.generate()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hire_name', help='The name of the hire')
    args = parser.parse_args()
    main(args)

