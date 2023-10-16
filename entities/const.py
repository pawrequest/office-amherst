from enum import Enum
from pathlib import Path


class DFLT:
    DEBUG = True
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
    INV_DIR_MOCK = GENERATED / 'mock_invoices'
    INV_DIR = INV_DIR_MOCK
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
    FREE_ITEMS = []


# class MAPS:
#     HIRE_ACC_BANDS = {
#