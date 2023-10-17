from decimal import Decimal

import pandas as pd
from win32com.gen_py import auto_cmc

from cmc.cmc_entities import Connection_e
from cmc.cmc_funcs import get_cmc, get_csr, get_fieldnames, qs_from_name, qs_to_lists
from cmc.commence import get_customer, hires_by_customer, sales_by_customer
from in_out.email_funcs import OutlookSender
from in_out.file_management import WordOpener
from managers.invoice import get_inv_temp
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


def get_many_customers():
    cmc = get_cmc()
    csr: auto_cmc.ICommenceCursor = cmc.GetCursor(0, 'Customer', 0)
    csr.SeekRow(0, 1000)
    qs = csr.GetQueryRowSet(20, 0)
    # for i in range(qs.RowCount):
    #     hires = hires_by_customer()
    lists = qs_to_lists(qs)
    return pd.DataFrame(lists, columns=get_fieldnames(qs))


def assess_get_customer_methods(hire):
    cuurs = get_csr('Customer')
    hire_name = hire.Name
    # customer = commence.qs_sngl(cuurs, hire['To Customer'])
    custoemr2 = get_customer(hire['To Customer'])
    # customer2 = commence.cust_of_transaction(hire_name, 'Hire')
    # assert customer.isequal(customer2)


def ass_make_sale_order():
    with TransactionContext() as tm_in:
        tm = tm_in
    sales = sales_by_customer('Test')
    ...


# ass_get_prices()
# ass_make_hire_order()
# ass_make_sale_order()

#
# def ass_main():
#     #     ...
#     fails_file_path = DFLT.GENERATED / 'fails.json'
#     with TransactionContext() as tm_in:
#         tm = tm_in
#     empty_order = list()
#     other = list()
#     empty_order_df = pd.concat(empty_order, axis=1).T
#     other_df = pd.concat(other, axis=1).T
#
#     hires = get_many_hires()
#     fails = pd.read_json(DFLT.GENERATED / 'fails.json')
#     fails = pd.concat({'empty_order': empty_order_df, 'other': other_df})
#     fails.to_json(fails_file_path)
#
#
#     for i in range(len(hires)):
#         hire = hires.iloc[[i]]
#         try:
#             inv = tm.hire_to_invoice(hire)
#             inv.generate()
#         except ValueError as e1:
#             empty_order.append(hire.iloc[0])
#             print(e1)
#             ...
#         except Exception as e:
#             ...
#             other.append(hire.iloc[0])
#
#     fails2 = pd.DataFrame([empty_order, other])
#     fails2.to_json(DFLT.GENERATED / 'fails2.json')
#
#



def get_con(record, connection: Connection_e):
    categories = []
    for connect in Connection_e:
        con_str = f"{connect.value.desc} {connect.value.value_table}"
        records = [
            qs_from_name(connect.value.key_table, record) for conn in Connection_e if con_str in record.keys()
        ]
        # todo ghetconnected item field call


