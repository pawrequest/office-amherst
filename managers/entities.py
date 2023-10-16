from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Iterable, List, Optional


class FIELDS(Enum):
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
class InventoryItem:
    name: str
    description: str


@dataclass
class FreeItem(InventoryItem):
    quantity: int

    def __str__(self):
        return f"{self.quantity} x {self.name}"


@dataclass
class Product(InventoryItem):
    price_each: Decimal

    def __str__(self):
        return f"{self.name} @ {self.price_each}"


@dataclass
class LineItem(Product):
    quantity: int

    @property
    def line_price(self):
        return self.price_each * int(self.quantity)

    def __str__(self):
        return f"{self.quantity} x {self.name} @ {self.price_each} = {self.line_price}"

    def __repr__(self):
        return f"LineItem({self.name} x {self.quantity})"


@dataclass
class Connection:
    name: str
    table: str
    fields: Optional[Iterable[str]] = None


@dataclass
class Order:
    customer: str
    line_items: List[LineItem] = field(default_factory=list)
    free_items: Optional[List[FreeItem]] = None
    tax_percent: int = 20
    shipping: Decimal = 15.00
    charity_percent: int = 0

    def __str__(self):
        return f"Order with {len(self.line_items)} lines for £{self.total}"

    @property
    def total_goods(self):
        return Decimal(sum(itm.line_price for itm in self.line_items))

    @property
    def charity_discount(self):
        if not self.charity_percent:
            return 0
        return Decimal(self.total_goods * self.charity_percent / 100)

    @property
    def subtotal(self):
        return Decimal(f"{sum([self.total_goods, Decimal(self.shipping)]) - self.charity_discount:.2f}")

    @property
    def tax(self):
        return Decimal(self.subtotal * self.tax_percent / 100)

    @property
    def total(self):
        return self.subtotal + self.tax



