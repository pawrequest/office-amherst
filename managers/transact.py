import json
import os
from _decimal import Decimal
from pprint import pprint

import pandas as pd

from in_out.excel import df_overwrite_wb
from managers.assets import decimal_from_value
from managers.entities import DFLT, FreeItem, HireOrder, LineItem, Order


class TransactionContext:
    def __init__(self, header_row=None, out_file=None, prices_wb=None, ):
        self.prcs_wb = prices_wb or DFLT.PRC_WB
        self.prcs_out = out_file or DFLT.PRC_OUT
        self.json_file = self.prcs_out.with_suffix('.json')  # JSON file path with new suffix
        self.header_row = header_row or int(DFLT.PRC_HEAD)
        self.df_bands, self.df_pr_hire, self.df_pr_sale= self.get_dfs()

    def __enter__(self):
        self.transaction_manager = TransactionManager(df_bands=self.df_bands, df_hire=self.df_pr_hire,
                                                      df_sale=self.df_pr_sale)
        return self.transaction_manager

    def get_dfs(self):
        assert self.prcs_wb.exists()

        # df_bands, df_hire, df_sale = self.dfs_from_json() if os.path.exists(self.json_file) else self.dfs_from_excel()
        df_bands, df_hire, df_sale = self.dfs_from_excel()
        return df_bands, df_hire, df_sale

    def dfs_from_excel(self):
        hire = pd.read_excel(self.prcs_wb, sheet_name='Hire', header=0,
                             dtype={'Min Qty': int, 'Min Duration': int},
                             converters={'Price': decimal_from_value})
        sale = pd.read_excel(self.prcs_wb, sheet_name='Sale', header=0,
                             dtype={'Min Qty': int},
                             converters={'Price': decimal_from_value})
        bands = pd.read_excel(self.prcs_wb, sheet_name='Bands', header=0,
                              dtype=str)

        return bands, hire, sale

    def dfs_from_json(self):
        with open(self.json_file, 'r') as json_file2:
            data = json.load(json_file2)

        hire = pd.DataFrame('df_hire')
        sale = pd.DataFrame('df_sale')
        bands = pd.DataFrame(data['df_b'], dtype=str)
        hire['Price'] = hire['Price'].apply(decimal_from_value)
        sale['Price'] = sale['Price'].apply(decimal_from_value)

        return bands, hire, sale

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if input("Save changes? (y/n)").lower() != 'y':
        #     return
        # self.dfs_to_json()
        # self.dfs_to_wb()
        ...

    def dfs_to_wb(self):
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


class TransactionManager:
    def __init__(self, df_bands: pd.DataFrame, df_hire: pd.DataFrame, df_sale: pd.DataFrame):
        self.df_bands = df_bands
        self.df_hire = df_hire
        self.df_sale = df_sale

    def make_hire_order(self, customer:pd.Series, hire: pd.Series, duration: int = None) -> HireOrder:
        duration = duration or int(hire['Weeks'])
        pay, free = self.parse_hire(hire)
        lineitems, free_items = [], []
        for name, qty in pay.items():
            description = self.get_description(name)
            price = self.get_hire_price(str(name), quantity=qty, duration=duration)
            long_name = f'{name}_hire_{duration}_weeks'
            lineitems.append(LineItem(name=long_name, description=description, price_each=price, quantity=qty))
        for name, qty in free.items():
            long_name = f'{name}_hire_{duration}_weeks'
            description = self.get_description(name)
            free_items.append(FreeItem(name=long_name, description=description, quantity=qty))

        order = HireOrder(line_items=lineitems, duration=duration, free_items=free_items, customer=customer['Name'])
        return order

    def make_sale_order(self, sale: pd.Series):
        lineitems = []
        order_items = items_from_sale(sale)
        for name_t, qty in order_items:
            name = str(name_t)
            price = self.get_sale_price(name, quantity=qty)
            description = self.get_description(name)
            lineitems.append(LineItem(name=name, description=description, price_each=price, quantity=qty))
        order = Order(line_items=lineitems)
        return order

    def get_sale_price(self, product_name: str, quantity: int):
        product_df = self.df_sale.loc[self.df_sale['Name'].str.lower() == product_name.lower()]
        return product_df.loc[product_df[DFLT.MIN_QTY].astype(int) <= int(quantity), 'Price'].min()

    def get_hire_price(self, product_name: str, quantity: int, duration: int):
        product = self.df_hire.loc[self.df_hire['Name'].str.lower() == str(product_name).lower()]
        if product.empty:
            prod_band = get_accessory_priceband(product_name)
            if prod_band is None:
                raise ValueError(f"No hire product or band found for {product_name}")
            product = self.df_hire.loc[self.df_hire['Name'].str.lower() == prod_band.lower()]
            if product.empty:
                raise ValueError(f"No hire product or band found for {product_name}")

        valid_products = product[
            (product['Min Qty'].astype(int) <= int(quantity)) & (product['Min Duration'].astype(int) <= int(duration))]

        if valid_products.empty:
            raise ValueError(f"No valid price for {product_name}")

        best_product = valid_products.sort_values(by=['Min Qty', 'Min Duration'], ascending=[False, False]).iloc[0]
        price = best_product['Price']
        return Decimal(f"{price:.2f}")


    def parse_hire(self, hire: pd.Series) -> (pd.Series, pd.Series):
        all_hire_items = all_item_fields(hire)
        hire_items = all_hire_items[all_hire_items.astype(int) > 0]
        # items_with = items_with_description(hire_items, self.df_bands)
        return pay_and_free_items(hire_items)

    def get_description(self, item_name: str):
        desc = self.df_hire.loc[self.df_hire['Name'].str.lower() == item_name.lower(), 'Description']
        if desc.empty:
            desc = self.df_bands.loc[self.df_bands['Name'].str.lower() == item_name.lower(), 'Description']
        if not desc.empty:
            desc = desc.iloc[0]
            return desc
        return ""
    # def get_description(self, item_name: str):
    #     desc = self.df_hire.loc[self.df_hire['Name'].str.lower() == item_name.lower(), 'Description']
    #     if desc.empty:
    #         desc = self.df_bands.loc[self.df_bands['Name'].str.lower() == item_name.lower(), 'Description']
    #     if len(desc) > 1:
    #         desc = desc.iloc[0]
    #     return desc[0]
    #

# def items_and_dur_from_hire(hire: pd.Series) -> ([tuple[str, int]], int):
#     duration = hire.loc['Weeks']
#     # items = [(field_name[7:], hire.loc[field_name])
#     #          for field_name in hire.index
#     #          if field_name.startswith('Number ') and int(hire.loc[field_name]) > 0]
#     items: tuple[pd.Series] = parse_hire_items(hire)
#     return items, duration


def all_item_fields(hire: pd.Series) -> pd.Series:
    items = hire[hire.index.str.startswith('Number ')]
    items.index = items.index.str[7:]
    return items




def pay_and_free_items(items: pd.Series) -> (pd.Series, pd.Series):
    pay_fields = ['UHF', 'EM', 'Cases', 'Icom', 'Wand', 'Batteries', 'EMC', 'Headset', 'Megaphone',
                  'ParrotRepeaterWand', 'VHF']
    free_fields = ['Magmount', 'UHF 6-way', 'Sgl Charger', 'Wand Battery']

    pay_items = items[items.index.isin(pay_fields)]
    free_items = items[items.index.isin(free_fields)]
    # accounted_fields = set(pay_fields) | set(free_fields)
    # unaccounted_fields = set(items.index) - accounted_fields
    # if unaccounted_fields:
    #     raise ValueError(f"Unaccounted fields: {list(unaccounted_fields)}")
    return pay_items, free_items


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
