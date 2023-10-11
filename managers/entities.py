from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Iterable, List, Optional

root = Path(__file__).parent.parent
templates = root / 'templates'
PRICES_WB = root / 'templates' / 'prices.xlsx'


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
    line_items: List[LineItem] = field(default_factory=list)
    free_items: Optional[List[FreeItem]] = None
    tax_percent: int = 20
    shipping: int = 15
    charity_percent: int = 0

    def __str__(self):
        return f"Order with {len(self.line_items)} lines for £{self.total}"


    @property
    def total_goods(self):
        return sum(itm.line_price for itm in self.line_items)

    @property
    def charity_discount(self):
        if not self.charity_percent:
            return 0
        return self.total_goods * self.charity_percent / 100

    @property
    def subtotal(self):
        return self.total_goods + self.shipping - self.charity_discount

    @property
    def tax(self):
        return self.subtotal * self.tax_percent / 100

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


class DFLT(Enum):
    MIN_DUR = 'Min Duration'
    MODEL = "Model"
    SERIAL = 'Barcode'
    ID = 'Number'
    FW = 'FW'
    FW_VERSION = 'XXXX'
    ROOT = Path(__file__).parent.parent
    DATA = ROOT / 'static/data'
    WB_AST = DATA / 'managers.xlsx'
    OUT_AST = DATA / 'assets_out.xlsx'
    SHEET_AST = 'Sheet1'
    HEAD_AST = 2
    WB_PRC = DATA / 'prices.xlsx'
    OUT_PRC = WB_PRC
    MIN_QTY = 'Min Qty'
    PRICE = 'Price'
    PRC_HEAD = 0



class DFLT2:
    MIN_DUR = 'Min Duration'
    MODEL = "Model"
    SERIAL = 'Barcode'
    ID = 'Number'
    FW = 'FW'
    FW_VERSION = 'XXXX'
    ROOT = Path(__file__).parent.parent
    DATA = ROOT / 'static/data'
    WB_AST = DATA / 'managers.xlsx'
    OUT_AST = DATA / 'assets_out.xlsx'
    SHEET_AST = 'Sheet1'
    HEAD_AST = 2
    WB_PRC = DATA / 'prices.xlsx'
    OUT_PRC = WB_PRC
    MIN_QTY = 'Min Qty'
    PRICE = 'Price'
    PRC_HEAD = 0
    INV_TMPLT = ROOT / 'static' / 'templates' / 'invoice_tmplt.docx'
    INV_OUT = ROOT / 'static' / 'templates' / 'invoice_out.docx'


class FIL_(Enum):
    FIELD = 'F'
    C_TO_ITEM = 'CTI'
    C_TO_CAT_TO_ITEM = 'CTCTI'
    C_TO_CAT_FIELD = 'CTCF'

