from decimal import Decimal

import pandas as pd
from win32com.gen_py import auto_cmc

from in_out import commence
from in_out.commence import get_fieldnames, hires_by_customer, qs_to_lists
from entities.abstract import DFLT
from entities.order import HireOrder
from managers.invoice import HireInvoice, next_inv_num
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
    cmc = commence.get_cmc()
    csr: auto_cmc.ICommenceCursor = cmc.GetCursor(0, 'Customer', 0)
    csr.SeekRow(0, 1000)
    qs = csr.GetQueryRowSet(1, 0)
    for i in range(len(qs)):
        hires = hires_by_customer()
    lists = qs_to_lists(qs)
    return pd.DataFrame(lists, columns=get_fieldnames(qs))


def assess_get_customer_methods(hire):
    cuurs = commence.get_csr('Customer')
    hire_name = hire.Name
    customer = commence.record_to_qs(cuurs, hire['To Customer'])
    customer2 = commence.cust_of_transaction(hire_name, 'Hire')
    assert customer.isequal(customer2)


def ass_make_sale_order():
    with TransactionContext() as tm_in:
        tm = tm_in
    sales = commence.sales_by_customer('Test')
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

def ass_main():
    fails_list = []
    success_list = []
    with TransactionContext() as tm_in:
        tm = tm_in
    hires = get_many_hires()
    for i in range(len(hires)):
        hire_name = hires.iloc[0].Name
        hire_rec = hires.iloc[[i]]
        hire = commence.hire(hire_name)
        try:
            inv = tm.hire_to_invoice(hire)
            inv.generate()
        except ValueError as e1:
            fail_series = hire.iloc[0].copy()
            fail_series['Fail Reason'] = str(e1)
            fails_list.append(fail_series)
        except Exception as e:
            # ... handle other exceptions similarly
            fail_series = hire.iloc[0].copy()
            fail_series['Fail Reason'] = str(e)
            fails_list.append(fail_series)
        else:
            success_list.append(hire.iloc[0].copy())



    # Create a DataFrame from the list of fail Series
    fails_df = pd.DataFrame(fails_list)
    success_list_df = pd.DataFrame(success_list)
    fails_df.to_json(DFLT.GENERATED / 'fails.json')
    success_list_df.to_json(DFLT.GENERATED / 'success.json')

    # hires = commence.hires_by_customer('Test')
    # hire = hires.head(1)
    # inv = tm.hire_to_invoice(hire)
    # inv.generate((DFLT.INV_DIR_MOCK))

    ...

ass_main()

