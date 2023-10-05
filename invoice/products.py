from decimal import Decimal

import pandas as pd

from excel.excel import pathy
from tmplt.entities import HirePrice, HireProduct, PRICES_WB, Price, SaleProduct


def get_all_sale_products(products_wb: pathy):
    df = pd.read_excel(products_wb, sheet_name='Sale', header=0)
    products = []
    for (product_name, product_description), product_group in df.groupby(['Name', 'Description']):
        prices = [Price(Decimal(str(row['Price'])), row['Min qty']) for index, row in product_group.iterrows()]
        products.append(SaleProduct(product_name, product_description, prices))
    return {p.name: p for p in products}


def get_all_hire_products(products_wb: pathy, ):
    df = pd.read_excel(products_wb, sheet_name='Hire', header=0)
    products = []
    for (product_name, product_description), product_group in df.groupby(['Name', 'Description']):
        prices = [HirePrice(Decimal(str(row['Price'])), row['Min qty'], row['Min Duration']) for index, row in product_group.iterrows()]
        products.append(HireProduct(product_name, product_description, prices))
    return {p.name: p for p in products}



