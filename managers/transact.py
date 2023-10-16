import json
from typing import List, Optional, Tuple

import pandas as pd

from in_out.excel import df_overwrite_wb
from in_out.commence import cust_of_transaction
from managers.entities import DTYPES, FreeItem, LineItem
from entities.abstract import DFLT
from entities.order import HireOrder
from managers.invoice import HireInvoice


class TransactionContext:
    def __init__(self, header_row=None, out_file=None, prices_wb=None, ):
        self.prcs_wb = prices_wb or DFLT.PRC_WB
        self.prcs_out = out_file or DFLT.PRC_OUT
        self.json_file = self.prcs_out.with_suffix('.json')  # JSON file path with new suffix
        self.header_row = header_row or int(DFLT.PRC_HEAD)
        self.df_bands, self.df_pr_hire, self.df_pr_sale = self.get_dfs()

    def __enter__(self):
        self.df_pr_hire['Price'] = self.df_pr_hire['Price'].apply(lambda x: x * 100)
        self.df_pr_sale['Price'] = self.df_pr_sale['Price'].apply(lambda x: x * 100)
        self.transaction_manager = TransactionManager(df_bands=self.df_bands, df_hire=self.df_pr_hire,
                                                      df_sale=self.df_pr_sale)
        return self.transaction_manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.df_pr_hire['Price'] = self.df_pr_hire['Price'].apply(lambda x: x / 100)
        self.df_pr_sale['Price'] = self.df_pr_sale['Price'].apply(lambda x: x / 100)

        # if input("Save changes? (y/n)").lower() != 'y':
        #     return
        # self.dfs_to_json()
        # self.dfs_to_wb()

    def get_dfs(self):
        assert self.prcs_wb.exists()

        # df_bands, df_hire, df_sale = self.dfs_from_json() if os.path.exists(self.json_file) else self.dfs_from_excel()
        df_bands, df_hire, df_sale = self.dfs_from_excel()
        return df_bands, df_hire, df_sale

    def dfs_from_excel(self):
        hire = pd.read_excel(self.prcs_wb, sheet_name='Hire', header=0,
                             dtype=DTYPES.HIRE)
        sale = pd.read_excel(self.prcs_wb, sheet_name='Sale', header=0,
                             dtype=DTYPES.SALE)
        bands = pd.read_excel(self.prcs_wb, sheet_name='Bands', header=0,
                              dtype=str)

        return bands, hire, sale

    def dfs_from_json(self):
        with open(self.json_file, 'r') as json_file2:
            data = json.load(json_file2)
        bands = pd.DataFrame(data['df_b'], dtype=str)
        hire = pd.DataFrame('df_hire')
        sale = pd.DataFrame('df_sale')

        return bands, hire, sale

    def dfs_to_wb(self):
        # todo convert back from 100
        df_overwrite_wb(input_workbook=DFLT.PRC_WB, sheet='Hire', header_row=0,
                        out_file=DFLT.PRC_OUT, df=self.df_pr_hire)
        df_overwrite_wb(input_workbook=DFLT.PRC_WB, sheet='Sale', header_row=0,
                        out_file=DFLT.PRC_OUT, df=self.df_pr_sale)
        df_overwrite_wb(input_workbook=DFLT.PRC_WB, sheet='Bands', header_row=0,
                        out_file=DFLT.PRC_OUT, df=self.df_bands)

    def dfs_to_json(self):
        data = {
            'df_hire': self.df_pr_hire.astype(str).to_dict(),
            'df_sale': self.df_pr_sale.astype(str).to_dict(),
            'df_b': self.df_bands.astype(str).to_dict(),
        }
        ...
        with open(self.json_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)


def get_hire_items(hire: pd.DataFrame):
    itm_cols = all_item_cols(hire)
    non_zero = itm_cols.loc[:, (itm_cols != 0).any(axis=0)]

    cleaned_data = itm_cols.dropna(axis=0, how='all')
    hire_items = cleaned_data.astype(int)

    hire_items = hire_items[hire_items > 0]
    return hire_items


def get_description(df_bands, df_hire, item_name: str):
    desc = df_hire.loc[df_hire['Name'].str.lower() == item_name.lower(), 'Description']
    if desc.empty:
        desc = df_bands.loc[df_bands['Name'].str.lower() == item_name.lower(), 'Description']
    if not desc.empty:
        desc = desc.iloc[0]
        return desc
    return ""


def get_hire_price(df_hire, product_name: str, quantity: int, duration: int):
    product = df_hire.loc[df_hire['Name'].str.lower() == str(product_name).lower()]
    if product.empty:
        prod_band = get_accessory_priceband(product_name)
        if prod_band is None:
            raise ValueError(f"No hire product or band found for {product_name}")
        product = df_hire.loc[df_hire['Name'].str.lower() == prod_band.lower()]
        if product.empty:
            raise ValueError(f"No hire product or band found for {product_name}")

    valid_products = product[
        (product['Min Qty'] <= quantity) & (product['Min Duration'] <= int(duration))]

    if valid_products.empty:
        raise ValueError(f"No valid price for {product_name}")

    best_product = valid_products.sort_values(by=['Min Qty', 'Min Duration'], ascending=[False, False]).iloc[0]
    price = best_product['Price']
    return price


def get_sale_price(df_sale, product_name: str, quantity: int):
    product_df = df_sale.loc[df_sale['Name'].str.lower() == product_name.lower()]
    return product_df.loc[product_df[DFLT.MIN_QTY].astype(int) <= int(quantity), 'Price'].min()


def get_hire_pay_items(df_h: pd.DataFrame, pay_items: pd.DataFrame, duration: int, df_bands: Optional[pd.DataFrame]):
    line_items = []
    for name, qty in pay_items.iloc[0].items():
        description = get_description(df_bands=df_bands, df_hire=df_h, item_name=name)
        price = get_hire_price(df_hire=df_h, product_name=name, quantity=qty, duration=duration)
        long_name = f'{name}_hire_{duration}_weeks'
        line_items.append(LineItem(name=long_name, description=description, price_each=price, quantity=int(qty)))
    return line_items


def get_free_hire_line_tems(df_bands, df_hire, duration, free_items):
    line_items = []
    for name, qty_ in free_items.items():
        qty = qty_[0]
        description = get_description(df_bands, df_hire, name)
        long_name = f'{name}_hire_{duration}_weeks'
        line_items.append(FreeItem(name=long_name, description=description, quantity=qty))
    return line_items


def lines_from_hire(df_bands, df_hire, hire: pd.DataFrame):
    duration = hire['Weeks'][0]
    hire_itms = filter_columns(hire)
    free = hire_itms.loc[:, hire_itms.columns.isin(DFLT.FREE_ITEMS)]
    pay = hire_itms.loc[:, ~hire_itms.columns.isin(DFLT.FREE_ITEMS)]  # ~ is used to negate the condition
    free_items = get_free_hire_line_tems(df_bands, df_hire, duration, free)
    line_items = get_hire_pay_items(df_h=df_hire, pay_items=pay, duration=duration, df_bands=df_bands)
    return line_items, free_items


class TransactionManager:
    def __init__(self, df_bands: pd.DataFrame, df_hire: pd.DataFrame, df_sale: pd.DataFrame):
        self.df_bands = df_bands
        self.df_hire = df_hire
        self.df_sale = df_sale

    def hire_to_invoice(self, hire: pd.DataFrame):
        customer = cust_of_transaction(hire.iloc[0].Name, 'Hire')
        line_items: Tuple[List, List] = lines_from_hire(self.df_bands, self.df_hire, hire)
        if not any([line_items[0], line_items[1]]):
            raise ValueError(f"No line items found for hire {hire.iloc[0].Name}")
        hire_order = HireOrder(customer=customer, line_items=line_items[0], free_items=line_items[1],
                               shipping=hire.iloc[0]['Delivery Cost'],
                               duration=hire.iloc[0].Weeks)
        return HireInvoice.from_hire(hire, hire_order, customer)

    # def sale_to_invoice(self, sale: pd.Series):
    #     customer = cust_of_transaction(sale.Name, 'Sale')
    #     line_items = lines_from_sale(self.df_bands, self.df_sale, sale)
    #     order = Order(customer.Name, line_items)
    #     invoice = SaleInvoice.from_sale(sale, order, customer)
    #     invoice.generate()


def all_item_fields(hire: pd.DataFrame) -> pd.DataFrame:
    items = hire[hire.index.str.startswith('Number ')]
    items.index = items.index.str[7:]
    return items


def all_item_cols(hire: pd.DataFrame) -> pd.DataFrame:
    item_columns = [col for col in hire.columns if col.startswith('Number ')]
    items = hire[item_columns].copy()
    items.columns = [col[7:] for col in item_columns]
    return items


def filter_columns(hire: pd.DataFrame) -> pd.DataFrame:
    # Get columns that have 'Number' in the name
    item_columns = [col for col in hire.columns if col.startswith('Number ')]

    # Keep only these columns
    hire_filtered = hire[item_columns]
    hire_filtered.columns = [col[7:] for col in item_columns]

    # Drop columns that have all zero or NaN values
    hire_filtered = hire_filtered.astype(int)
    hire_filtered = hire_filtered.loc[:, (hire_filtered != 0).any(axis=0)]

    return hire_filtered


def get_accessory_priceband(accessory_name: str):
    if accessory_name in ["EM", 'Parrot', 'Battery', 'Batteries', 'Cases']:
        return "Accessory A"
    elif accessory_name in ['EMC', 'Headset']:
        return "Accessory B"
    elif accessory_name in ['Aircraft']:
        return "Accessory C"
    elif accessory_name == 'Icom':
        return 'Mobile'
    elif accessory_name == 'Wand':
        return 'Wand'
    elif accessory_name == 'Megaphone':
        return 'Megaphone'
    else:
        return None


def items_from_sale(sale: pd.Series):
    all_items = sale.loc['Items Ordered']
    item_lines = all_items.split('\r\n')
    item_tups = []
    for line in item_lines:
        res = line.split(' x ')
        if len(res) != 2:
            continue
        item_name, qty = res
        item_tups.append((item_name, int(qty)))
    return item_tups


