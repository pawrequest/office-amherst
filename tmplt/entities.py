from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Iterable, List, Optional

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
        "Name",
    ]
    SALE = [
        "Invoice Address",
        'Name',
    ]


@dataclass
class Price:
    price: Decimal
    min_quantity: int
    min_duration: int = 0


@dataclass
class HirePrice(Price):
    min_duration: int


@dataclass
class Product:
    name: str
    description: str
    prices: List[Price]

    def get_sale_price(self, quantity):
        if all([p.min_quantity != 0 for p in self.prices]):
            raise ValueError(f"Product {self.name} is not available for sale (min_duration must = 0 for sale)")
        valid_prices = [p for p in self.prices if p.min_quantity <= quantity]
        return min([p.price for p in valid_prices])

    def get_hire_price(self, quantity, duration):
        if all([p.min_duration == 0 for p in self.prices]):
            raise ValueError(f"Product {self.name} is not available for hire")
        valid_prices = [p for p in self.prices if p.min_quantity <= quantity and p.min_duration <= self.duration]
        actual_price = min([p.price for p in valid_prices])
        return quantity * actual_price


@dataclass
class LineItemABC:
    product: Product
    quantity: int

    @property
    def line_price(self):
        raise NotImplementedError


@dataclass
class Connection:
    name: str
    table: str
    fields: Optional[Iterable[str]] = None



@dataclass
class SaleLineItem(LineItemABC):
    product: Product

    @property
    def line_price(self):
        return self.product.get_sale_price(self.quantity) * self.quantity


@dataclass
class HireLineItem:
    product: Product
    quantity: int
    duration: int

    @property
    def price_each(self):
        return self.product.get_hire_price(self.quantity, self.duration)

    @property
    def line_price(self):
        return self.price_each * self.quantity


@dataclass
class Hire:
    line_items = List[HireLineItem]


class Connections(Enum):
    CUSTOMER_SALES = Connection(name="Has Hired", table='Hire')
    CUSTOMER_HIRES = Connection(name="Involves", table='Sale')
    # HIRES_CUSTOMER = Connection(name="To", table='Customer')
    # SALES_CUSTOMER = Connection(name="To", table='Customer')
    TO_CUSTOMER = Connection(name="To", table='Customer')


