from managers.cmc_manager import CommenceContext
from managers.tran_manager import TransactionContext
from managers.entities import SaleOrder, HireOrder


def test_main():
    with CommenceContext() as cmc:
        cust = cmc.customer('Test')
        sales = cmc.sales_customer('Test')
        sale = sales.iloc[0]
        hires = cmc.hires_customer('Test')
        hire = hires.iloc[0]

    with TransactionContext() as tm:
        hire_order = tm.make_hire_order(hire, 1)
        sale_order = tm.make_sale_order(sale)

    assert isinstance(hire_order, HireOrder)
    assert isinstance(sale_order, SaleOrder)
