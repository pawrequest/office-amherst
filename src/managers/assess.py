from decimal import Decimal

import pandas as pd
from win32com.gen_py import auto_cmc

from cmc.commence import CmcContext
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


# def get_many_customers():
#     cmc = get_cmc()
#     csr: auto_cmc.ICommenceCursor = cmc.GetCursor(0, 'Customer', 0)
#     csr.SeekRow(0, 1000)
#     qs = csr.GetQueryRowSet(20, 0)
#     # for i in range(qs.RowCount):
#     #     hires = hires_by_customer()
#     lists = qs_to_lists(qs)
#     return pd.DataFrame(lists, columns=get_fieldnames(qs))


# def assess_get_customer_methods(hire):
#     with CmcContext() as cmc:
#         hire_name = hire.Name
#     # customer = commence.qs_sngl(cuurs, hire['To Customer'])
#     custoemr2 = get_customer(hire['To Customer'])
#     # customer2 = commence.cust_of_transaction(hire_name, 'Hire')
#     # assert customer.isequal(customer2)


# def ass_make_sale_order():
#     with TransactionContext() as tm_in:
#         tm = tm_in
#     sales = sales_by_customer('Test')
#     ...


# ass_get_prices()
# ass_make_hire_order()
# ass_make_sale_order()



# def get_con(record, connection: Connection_e):
#     categories = []
#     for connect in Connection_e:
#         con_str = f"{connect.value.desc} {connect.value.value_table}"
#         records = [
#             qs_from_name(connect.value.key_table, record) for conn in Connection_e if con_str in record.keys()
#         ]
#         # todo ghetconnected item field call
#
#
