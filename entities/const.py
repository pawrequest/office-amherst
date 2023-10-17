from enum import Enum
from pathlib import Path

from in_out.email_funcs import Email


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
    PRC_OUT = GENERATED / 'prices_out.xlsx'
    INV_TMPLT = TEMPLATE / 'invoice_tmplt.docx'
    INV_DIR_MOCK = GENERATED / 'mock_invoices'
    INV_OUT_DIR = INV_DIR_MOCK
    INV_DIR = Path(r'R:\ACCOUNTS\invoices')
    TEMP_INV = INV_OUT_DIR / '_temp_invoice.docx'
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
    INV_EMAIL_OBJ:Email = Email(
        to_address='pythonsnake48@gmail.com',
        subject='Invoice',
        body='Please find attached the invoice for your hire.',
    )


class FILTER_(Enum):
    FIELD = 'F'
    C_TO_ITEM = 'CTI'
    C_TO_CAT_TO_ITEM = 'CTCTI'
    C_TO_CAT_FIELD = 'CTCF'


NOT_HIRE = ['Min Duration', 'Closed']


class DTYPES:
    HIRE_PRICES = {
        'Name': 'string',
        'Description': 'string',
        'Min Qty': 'int',
        'Min Duration': 'int',
        'Price': 'float',

    }
    HIRE_RECORD = {
        'Items': 'string',
        'Closed': 'bool',
        'Reference Number': 'string',
        'Weeks': 'int',
        'Boxes': 'int',
        'Recurring': 'bool',
        'Delivery Cost': 'float',
    }
    SALE_PRICES = {key: value for key, value in HIRE_PRICES.items() if key != 'Min Duration'}


class FIELDS:
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
    FREE_ITEMS = ['Sgl Charger', 'UHF 6-way', 'Wand Battery']

# class MAPS:
#     HIRE_ACC_BANDS = {
#
def format_currency(value):
    # return value
    # return f' £ {value:.2f}'
    if value == '':
        return ''
    # if isinstance(value, str):
    #     value = Decimal(value)
    return f"£{value:>8.2f}"


