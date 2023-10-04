from dataclasses import dataclass
from decimal import Decimal
from typing import List, Literal

import pandas as pd

from excel.excel import pathy


@dataclass
class Price:
    price: Decimal
    min_quantity: int


@dataclass
class ProductABC:
    name: str
    description: str


@dataclass
class SaleProduct(ProductABC):
    prices: List[Price]

    def get_price(self, quantity):
        valid_prices = [p for p in self.prices if p.min_quantity <= quantity]
        return min([p.price for p in valid_prices])


def get_all_sale_products(products_wb: pathy):
    df = pd.read_excel(products_wb, sheet_name='Sale', header=0)
    products = []
    for (product_name, product_description), product_group in df.groupby(['Name', 'Description']):
        prices = [Price(Decimal(str(row['Price'])), row['Min qty']) for index, row in product_group.iterrows()]
        products.append(SaleProduct(product_name, product_description, prices))
    return products


@dataclass
class SaleLineItem:
    product: SaleProduct
    quantity: int

    @property
    def line_price(self):
        return self.product.get_price(self.quantity) * self.quantity


@dataclass
class HirePrice(Price):
    min_duration: int


@dataclass
class HireProduct(ProductABC):
    prices: List[HirePrice]

    def get_price(self, quantity, duration):
        valid_prices = [p for p in self.prices if p.min_quantity <= quantity and p.min_duration <= duration]
        actual_price = min([p.price for p in valid_prices])
        return quantity * actual_price

def get_all_hire_products(products_wb: pathy, ):
    df = pd.read_excel(products_wb, sheet_name='Hire', header=0)
    products = []
    for (product_name, product_description), product_group in df.groupby(['Name', 'Description']):
        prices = [HirePrice(Decimal(str(row['Price'])), row['Min qty'], row['Min Duration']) for index, row in product_group.iterrows()]
        products.append(HireProduct(product_name, product_description, prices))
    return {p.name: p for p in products}


prices_wb = r'C:\paul\office_am\input_files\prices.xlsx'
pro = get_all_sale_products(prices_wb)
price1 = pro[0].get_price(1)
price11 = pro[0].get_price(11)
hire_pro = get_all_hire_products(prices_wb)
hire_price1_1 = hire_pro['UHF'].get_price(quantity=1, duration=1)

...
