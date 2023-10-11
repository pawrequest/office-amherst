import argparse

from managers.asset_manager import AssetManager
from managers.cmc_manager import Commence, CommenceContext
from managers.tran_manager import TransactionManager, TransactionContext
import win32com.client



def main():

    with CommenceContext() as cmc:
        cust = cmc.customer('Test')
        sales = cmc.sales_customer('Test')
        sale = sales.iloc[0]
        hires = cmc.hires_customer('Test')
        hire = hires.iloc[0]

    with TransactionContext() as tm:
        hire_order = tm.make_hire_order(hire, 1)
        sale_order = tm.make_sale_order(sale)

    ...

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--id_data', help='List of data to match')
    # args = parser.parse_args()
    main()
