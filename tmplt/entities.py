from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Iterable, List

root = Path(__file__).parent.parent
templates = root / 'tmplt'
PRICES_WB = root / 'tmplt' / 'prices.xlsx'


class Fields(Enum):
    CUSTOMER = [
        "Contact Name",
        "Name",
        "Address",
        "Postcode",
        "Charity?",
        "Discount Percentage",
        "Email",
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


class Connections(Enum):
    CUSTOMER_SALES = Connection(name="Has Hired", table='Hire', fields=Fields.HIRE.value)
    CUSTOMER_HIRES = Connection(name="Involves", table='Sale', fields=Fields.SALE.value)
    # HIRES_CUSTOMER = Connection(name="To", table='Customer', fields=Fields.CUSTOMER.value)
    # SALES_CUSTOMER = Connection(name="To", table='Customer', fields=Fields.CUSTOMER.value)
    TO_CUSTOMER = Connection(name="To", table='Customer', fields=Fields.CUSTOMER.value)
