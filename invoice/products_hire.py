from dataclasses import dataclass
from typing import List

from tmplt.entities import Price, ProductABC


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


# def hire_invoice(hire_name):
#     hire_data = get_hire_data_inv(hire_name)
#     products = get_all_products(products_wb='/input_files/prices.xlsx', category='Hire')
#     return hire_data

#
# def line_items_from_hire(products: Iterable[ProductABC], hire_data):
#     line_items = []
#     duration = hire_data['data']['Weeks']
#
#     for k, v in hire_data['data'].items():
#         if k.startswith('Number'):
#             product_name = k.split('Number ')[1]
#             quantity = int(v)
#             product = [p for p in products if p.name == product_name][0]
#             line_item = LineItem(product, quantity)
#             line_items.append(line_item)
#     return line_items
