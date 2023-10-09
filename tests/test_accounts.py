import os
from pathlib import Path

import pandas as pd

from account.check_invoice_paid import check_paid

# AC_WORKBOOK = r"R:\ACCOUNTS\ye2023\ac2223.xls"
AC_WORKBOOK = Path(r'..\tmplt\ac2223.xls')
INVOICE_DOC = Path(r"R:\ACCOUNTS\invoices\a24160.docx")

def test_check_paid():
    workbook = AC_WORKBOOK
    invoice_doc = INVOICE_DOC
    if isinstance(invoice_doc, Path):
        invoice_doc = os.path.splitext(os.path.basename(invoice_doc))[0]
    df = pd.read_excel(workbook, sheet_name='Sales', header=2)
    result = check_paid(df, invoice_doc)
    assert isinstance(result, str)
