from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from pathlib import Path
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


@dataclass
class HireOrder(Order):
    duration: int = 1

    def __str__(self):
        return f"Order for {self.duration} weeks with {len(self.line_items)} lines for £{self.total}"


class Connections(Enum):
    CUSTOMER_HIRES = Connection(name="Has Hired", table='Hire')
    CUSTOMER_SALES = Connection(name="Involves", table='Sale')
    TO_CUSTOMER = Connection(name="To", table='Customer')



class DFLT:
    ROOT = Path(__file__).parent.parent
    STATIC = ROOT / 'static'
    DATA = STATIC / 'data'
    GENERATED = STATIC / 'generated'
    TEMPLATE = STATIC / 'templates'
    FW_VERSION = 'XXXX'
    AST_WB = DATA / 'assets.xlsx'
    PRC_WB = DATA / 'prices.xlsx'
    AST_OUT = GENERATED / 'assets_out.xlsx'
    INV_TMPLT = TEMPLATE / 'invoice_tmplt.docx'
    PRC_OUT = GENERATED / 'prices_out.xlsx'
    INV_OUT = GENERATED / 'invoice_out.docx'
    MIN_DUR = 'Min Duration'
    MODEL = "Model"
    SERIAL = 'Barcode'
    ID = 'Number'
    FW = 'FW'
    MIN_QTY = 'Min Qty'
    PRICE = 'Price'
    AST_SHEET = 'Sheet1'
    AST_HEAD = 2
    PRC_HEAD = 0


class FILTER_(Enum):
    FIELD = 'F'
    C_TO_ITEM = 'CTI'
    C_TO_CAT_TO_ITEM = 'CTCTI'
    C_TO_CAT_FIELD = 'CTCF'
