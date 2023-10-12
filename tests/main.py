from win32com.client.gencache import EnsureDispatch
import datetime

from managers.cmc_manager import CommenceContext
from managers.invoice_manager import Address1, HireDates, HireInvoice
from managers.tran_manager import TransactionContext
from managers.entities import HireOrder, Order

#
# def test_main():
#     with CommenceContext() as cmc:
#         cust = cmc.customer('Test')
#         sales = cmc.sales_by_customer('Test')
#         hires = cmc.hires_by_customer('Test')
#         sale = sales.iloc[0]
#         hire = hires.iloc[0]
#         hire4 = cmc.hire("RAC Saddle Club Office - 05/09/2023 ref 19713")
#         sale2 = cmc.sale('Truckline Services - 26/10/2022 ref 11')
#         ...
#
#     # with TransactionContext() as tm:
#     #     hire_order = tm.make_hire_order(hire, 1)
#     #     hire_order2 = tm.make_hire_order(hire2, 1)
#     #     sale_order = tm.make_sale_order(sale)
#     #     sale_order = tm.make_sale_order(sale2)
#     #
#     # invoice = HireInvoice.from_hire(hire, hire_order)
#     # invoice.generate()
#     # ...
#
#     # assert isinstance(hire_order_test, HireOrder)
#     # assert isinstance(sale_order, Order)
#


