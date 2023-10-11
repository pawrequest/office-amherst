from dataclasses import dataclass

from _decimal import Decimal

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
    def __init__(self, df_pr_hire, df_pr_sale):
        self.df_hire = df_pr_hire
        self.df_sale = df_pr_sale

    def make_hire_order(self, hire_dict, duration):
        lineitems = []

        for name, qty in hire_dict.items():
            price = self.get_hire_price(name, quantity=qty, duration=duration)
            name = f'{name}_hire_{duration}_weeks'
            product = Product(name=name, description='desc', price_each=price)
            lineitems.append(LineItem(product=product, quantity=qty))
        order = HireOrder(line_items=lineitems, duration=duration)
        return order

    def make_sales_order(self, sale_dict):
        lineitems = []
        for name, qty in sale_dict.items():
            price = self.get_sale_price(name, quantity=qty)
            product = Product(name=name, description='desc', price_each=price)
            lineitems.append(LineItem(product=product, quantity=qty))

        order = Order(line_items=lineitems)
        return order

    def get_sale_price(self, product_name: str, quantity: int):
        product_df = self.df_sale.loc[self.df_sale['Name'] == product_name]
        return product_df.loc[product_df[DFLT.MIN_QTY.value] <= quantity, 'Price'].min()

    def get_hire_price(self, product_name: str, quantity: int, duration: int):
        product = self.df_hire.loc[self.df_hire['Name'] == product_name]
        valid_products = product[(product['Min Qty'] <= quantity) & (product['Min Duration'] <= duration)]
        if valid_products.empty:
            raise ValueError(f"No valid price found for {duration} weeks x {quantity} units of {product_name}")
        best_product = valid_products.sort_values(by=['Min Qty', 'Min Duration'], ascending=[False, False]).iloc[0]
        price = best_product['Price']
        return Decimal(price)



def items_and_dur_from_hire(hire: pd.Series):
    duration = hire.loc['Weeks']
    items = [(field_name[7:], hire.loc[field_name])
             for field_name in hire.index
             if field_name.startswith('Number ') and int(hire.loc[field_name]) > 0]
    return items, duration