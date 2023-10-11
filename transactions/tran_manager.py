from _decimal import Decimal
from dataclasses import dataclass

import pandas as pd

from assets.entities import DFLT, LineItem, Product


@dataclass
class Order:
    line_items: [LineItem]

    @property
    def total_price(self):
        return sum([itm.line_price for itm in self.line_items])

    def __str__(self):
        return f"Order for {len(self.line_items)} products: {self.line_items}"


@dataclass
class HireOrder(Order):
    duration: int

    def __str__(self):
        return f"Order for {self.duration} weeks: {self.line_items}"


class TransactionManager:
    def __init__(self, df_pr_hire: pd.DataFrame, df_pr_sale: pd.DataFrame, df_bands: pd.DataFrame):
        self.df_hire = df_pr_hire
        self.df_sale = df_pr_sale
        self.df_bands = df_bands

    def make_hire_order(self, hire: pd.Series, duration: int = None) -> HireOrder:
        pay, free = self.parse_hire(hire)
        lineitems = []
        for name, qty in pay.items():
            price = self.get_hire_price(str(name), quantity=qty, duration=duration)
            name = f'{name}_hire_{duration}_weeks'
            product = Product(name=name, description='desc', price_each=price)
            lineitems.append(LineItem(product=product, quantity=qty))
        order = HireOrder(line_items=lineitems, duration=duration)
        return order

    def make_sales_order(self, sale: pd.Series):
        lineitems = []
        order_items = items_from_sale(sale)
        for name_t, qty in order_items:
            name = str(name_t)
            price = self.get_sale_price(name, quantity=qty)
            product = Product(name=name, description='desc', price_each=price)
            lineitems.append(LineItem(product=product, quantity=qty))

        order = Order(line_items=lineitems)
        return order

    def get_sale_price(self, product_name: str, quantity: int):
        product_df = self.df_sale.loc[self.df_sale['Name'].str.lower() == product_name.lower()]
        return product_df.loc[product_df[DFLT.MIN_QTY.value] <= quantity, 'Price'].min()

    def get_hire_price(self, product_name: str, quantity: int, duration: int):
        product = self.df_hire.loc[self.df_hire['Name'] == product_name]
        if product.empty:
            prod_band = self.df_bands.loc[self.df_bands['Name'] == 'EM', 'Band'].values[0]
            product = self.df_hire.loc[self.df_hire['Name'] == prod_band]
            if product.empty:
                raise ValueError(f"No hire product or band found for {product_name}")

        valid_products = product[(product['Min Qty'] <= int(quantity)) & (product['Min Duration'] <= int(duration))]

        if valid_products.empty:
                raise ValueError(f"No val;id price for {product_name}")

        best_product = valid_products.sort_values(by=['Min Qty', 'Min Duration'], ascending=[False, False]).iloc[0]
        price = best_product['Price']
        return Decimal(price)

    def parse_hire(self, hire:pd.Series):
        all_hire_items = all_item_fields(hire)
        hire_items = all_hire_items[all_hire_items.astype(int) > 0]
        return pay_and_free_items(hire_items)




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
    pay_fields = [
        'UHF',
        'EM',
        'Cases',
        'Icom'
        'Batteries',
        'EMC',
        'Headset',
        'Megaphone',
        'Parrot'
        'Repeater'
        'Wand',
        'VHF'
    ]
    free_fields = [
        'Magmount',
        'UHF 6-way',
        'Sgl Charger'
    ]
    pay_items = items[items.index.isin(pay_fields)]
    free_items = items[items.index.isin(free_fields)]
    return pay_items, free_items


# def get_accessory_priceband(accessory_name: str):
#     if accessory_name in ["EM", 'Parrot', 'Battery', 'Cases']:
#         return "Accessory A"
#     elif accessory_name in ['EMC', 'Headset']:
#         return "Accessory B"
#     elif accessory_name in ['Aircraft']:
#         return "Accessory C"
#     else:
#         return None


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
