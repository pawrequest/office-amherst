import os

import pandas as pd

from account.check_invoice_paid import check_paid


def test_check_paid():
    workbook = r"R:\ACCOUNTS\ye2023\ac2223.xls"
    id_data = r"R:\ACCOUNTS\invoices\a24160.docx"
    if os.path.isfile(id_data):
        id_data = os.path.splitext(os.path.basename(id_data))[0]
    df = pd.read_excel(workbook, sheet_name='Sales', header=2)
    result = check_paid(df, id_data)
    assert isinstance(result, str)
