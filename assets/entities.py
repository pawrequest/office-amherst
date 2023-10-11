from dataclasses import dataclass
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
class Product:
    name: str
    description: str
    price_each:Decimal


@dataclass
class LineItem:
    product: Product
    quantity: int

    @property
    def line_price(self):
        return self.product.price_each * self.quantity
    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.product.price_each} = {self.line_price}"

@dataclass
class Connection:
    name: str
    table: str
    fields: Optional[Iterable[str]] = None




@dataclass
class Order:
    line_items = List[LineItem]


class Connections(Enum):
    CUSTOMER_HIRES = Connection(name="Has Hired", table='Hire')
    CUSTOMER_SALES = Connection(name="Involves", table='Sale')
    # HIRES_CUSTOMER = Connection(name="To", table='Customer')
    # SALES_CUSTOMER = Connection(name="To", table='Customer')
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
    WB_AST = DATA / 'assets.xlsx'
    OUT_AST = DATA / 'assets_out.xlsx'
    SHEET = 'Sheet1'
    HEAD = 2
    WB_PRC = DATA / 'prices.xlsx'
    OUT_PRC = WB_PRC
    MIN_QTY = 'Min Qty'
    PRICE = 'Price'


class FIL_(Enum):
    FIELD = 'F'
    C_TO_ITEM = 'CTI'
    C_TO_CAT_TO_ITEM = 'CTCTI'
    C_TO_CAT_FIELD = 'CTCF'
