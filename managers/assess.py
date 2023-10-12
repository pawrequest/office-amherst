from decimal import Decimal

from managers import commence
from managers.entities import DFLT, HireOrder
from managers.invoice import HireInvoice
from managers.transact import TransactionContext


def ass_get_prices():
    with TransactionContext() as tm_in:
        tm = tm_in
    price = tm.get_sale_price('H405', 1)
    hire_price = tm.get_hire_price('UHF', 1, 1)
    assert isinstance(price, Decimal)
    assert isinstance(hire_price, Decimal)
    assert hire_price < price


# def test_make_sale_order(tm_fxt, sale_cursor_fxt):
#     sales = cmc_manager.sales_by_customer('Test')
#     sale = sales.iloc[0]
#     sale_order = tm_fxt.make_sale_order(sale)
#     ...


def ass_make_hire_order():
    with TransactionContext() as tm_in:
        tm = tm_in

    hires = commence.hires_by_customer('Test')
    hire = hires.iloc[0]
    hire_name = hire.Name
    customer = commence.cust_of_transaction(hire_name, 'Hire')
    hire_order = tm.make_hire_order(customer=customer, hire=hire)
    assert isinstance(hire_order, HireOrder)
    invoice = HireInvoice.from_hire(hire, hire_order, customer)
    invoice.generate()
    assert DFLT.INV_OUT.is_file()
    assert '.docx' in DFLT.INV_OUT.suffixes


ass_get_prices()
ass_make_hire_order()
