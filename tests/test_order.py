import shutil
import tempfile
from pathlib import Path

import pytest

from office_am.cmc.commence import CmcContext
from office_am.office_tools.o_tool import OfficeTools
from office_am.order.invoice import get_inv_temp
from office_am.order.order_ent import LineItem
from office_am.order.transact import TransactionContext



@pytest.mark.parametrize("office_tool_method", [OfficeTools.microsoft, OfficeTools.libre])
def test_office_tools(office_tool_method):
    ot = office_tool_method()
    temp_dir = tempfile.mkdtemp()
    outfile = Path(temp_dir) / "outfile.docx"

    with CmcContext() as cmc:
        hires = cmc.hires_by_customer('Test')
        hire = hires[0]

        with TransactionContext() as tm:
            hire_inv = tm.get_hire_invoice(hire)
            assert isinstance(hire_inv.order.line_items[0], LineItem)
            template, temp_file_ = get_inv_temp(hire_inv)
            shutil.copy(temp_file_, outfile)
            pdf_file = ot.pdf.from_docx(outfile)
            assert pdf_file.is_file()
