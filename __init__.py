from pathlib import Path

from in_out.email_funcs import Email

DEBUG = True

class DFLT_PATHS:
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


class DFLT_CONST:
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


DFLT_EMAIL_O:Email = Email(
        to_address='pythonsnake48@gmail.com',
        subject='Invoice',
        body='Please find attached the invoice for your hire.',
    )
