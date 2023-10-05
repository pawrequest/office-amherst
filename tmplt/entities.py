from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Iterable, List


class Fields(Enum):
    CUSTOMER = [
        "Contact Name",
        "Name",
        "Address",
        "Postcode",
    ]
    HIRE = [
        "Delivery Contact",
        "Delivery Name",
        "Delivery Address",
        "Delivery Postcode",
        "Number UHF",
        "Booked Date",
        'Name',
    ]
    SALE = [
        "Invoice Address",
        'Name',
    ]


@dataclass
class Connection:
    name: str
    table: str
    fields: Iterable[str]


root = Path(__file__).parent.parent
templates = root / 'tmplt'
PRICES_WB = root / 'input_files' / 'prices.xlsx'


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
