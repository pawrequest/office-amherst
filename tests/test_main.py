import datetime

from managers.cmc_manager import CommenceContext
from managers.invoice_manager import Address1, HireDates, HireInvoice
from managers.tran_manager import TransactionContext
from managers.entities import HireOrder, Order


def test_main():
    with CommenceContext() as cmc:
        # cust = cmc.customer('Test')
        # sales = cmc.sales_customer('Test')
        # sale = sales.iloc[0]
        # hires = cmc.hires_customer('Test')
        # hire = hires.iloc[0]
        # hire3 = cmc.hire("Test - 16/08/2023 ref 31619")
        hire2 = cmc.hire("TGI - 23/09/2022 ref 19527")

    with TransactionContext() as tm:
        hire_order = tm.make_hire_order(hire2, 1)
        # hire_order_test = tm.make_hire_order(hire, 1)
        # sale_order = tm.make_sale_order(sale)

    invoice = HireInvoice.from_hire(hire2, hire_order)
    invoice.generate()
    ...

    # assert isinstance(hire_order_test, HireOrder)
    # assert isinstance(sale_order, Order)

