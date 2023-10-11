
from in_out.cmc_direct import Commence
from transactions.tran_manager import HireOrder, items_and_dur_from_hire


def test_cmc_direct():
    cmc = Commence()
    hires = cmc.customer_hires('Test')
    hire = hires.iloc[0]
    items, duration = items_and_dur_from_hire(hire)
    sales = cmc.customer_sales('Amersham School')
    sale = sales.iloc[0]

    order = HireOrder(items, duration)
    hire1 = cmc.hire(r'Test - 10/11/2023 ref 42744 ')

    sale1 = cmc.sale(r'Amersham School - 17/01/2023 ref 90')

    ...


