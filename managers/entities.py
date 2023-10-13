from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd

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
        return int(self.price_each * self.quantity)

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
    customer: pd.DataFrame
    line_items: List[LineItem] = field(default_factory=list)
    free_items: Optional[List[FreeItem]] = None
    tax_percent: int = 20
    shipping: int = 15.00
    charity_percent: int = 0
    duration: Optional[int] = None

    # def __str__(self):
    #     return f"Order with {len(self.line_items)} lines for £{self.total}"

    @property
    def total_goods(self) ->int:
        res = int(sum(itm.line_price for itm in self.line_items))
        return res

    @property
    def charity_discount(self) -> int:
        if not self.charity_percent:
            return 0
        i = int(self.total_goods * self.charity_percent / 100)
        return i

    @property
    def subtotal(self) -> int:
        sub = int(self.total_goods + self.shipping - self.charity_discount)
        return sub

    @property
    def tax(self) -> int:
        i = int(self.subtotal * self.tax_percent / 100)
        return i

    @property
    def total(self) -> int:
        tot = int(self.subtotal + self.tax)
        return tot


class HireOrder(Order):
    duration: int
    #
    # def __str__(self):
    #     return f"Order for {self.duration} weeks with {len(self.line_items)} lines for £{self.total}"


class Connections(Enum):
    CUSTOMER_HIRES = Connection(name="Has Hired", table='Hire')
    CUSTOMER_SALES = Connection(name="Involves", table='Sale')
    TO_CUSTOMER = Connection(name="To", table='Customer')


# class DFLT(Enum):
#     MIN_DUR = 'Min Duration'
#     MODEL = "Model"
#     SERIAL = 'Barcode'
#     ID = 'Number'
#     FW = 'FW'
#     FW_VERSION = 'XXXX'
#     ROOT = Path(__file__).parent.parent
#     DATA = ROOT / 'static/data'
#     WB_AST = DATA / 'managers.xlsx'
#     OUT_AST = DATA / 'assets_out.xlsx'
#     SHEET_AST = 'Sheet1'
#     HEAD_AST = 2
#     WB_PRC = DATA / 'prices.xlsx'
#     OUT_PRC = WB_PRC
#     MIN_QTY = 'Min Qty'
#     PRICE = 'Price'
#     PRC_HEAD = 0


class DFLT:
    DEBUG = True
    INV_DIR = Path(r'R:\ACCOUNTS\invoices')
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
    INPUTS = STATIC / 'input_files'
    INV_DIR_MOCK = GENERATED / 'mock_invoices'
    FREE_ITEMS = ['Magmount', 'UHF 6-way', 'Sgl Charger', 'Wand Battery']


class FILTER_(Enum):
    FIELD = 'F'
    C_TO_ITEM = 'CTI'
    C_TO_CAT_TO_ITEM = 'CTCTI'
    C_TO_CAT_FIELD = 'CTCF'


class DTYPES:
    HIRE = {
        'Name': 'string',
        'Description': 'string',
        'Min Qty': 'int',
        'Min Duration': 'int',
        'Price': 'int',
        'Items': 'string',
        'Closed': 'bool',
        'Reference Number': 'string',
        'Weeks': 'int',
        'Boxes': 'int',
        'Recurring': 'bool',

    }
    SALE = {key: value for key, value in HIRE.items() if key != 'Min Duration'}
