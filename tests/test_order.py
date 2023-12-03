import shutil
from pathlib import Path

from cmc.commence import CmcContext
from office_am.dflt import DFLT_PATHS
from office_am.main import do_cmc, do_email
from office_tools.o_tool import OfficeTools, get_installed_combinations
from office_am.order.invoice import get_inv_temp
from office_am.order.order_ent import LineItem
from office_am.order.transact import TransactionContext
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest


@pytest.mark.parametrize("office_tool_instance", get_installed_combinations())
def test_office_tools(office_tool_instance):

    with TemporaryDirectory() as temp_dir:
        tempy = Path(temp_dir) / 'temp.docx'

        ot = office_tool_instance
        with CmcContext() as cmc:
            hire = cmc.hires_by_customer('Test')[0]

            with TransactionContext() as tm:
                hire_inv = tm.get_hire_invoice(hire)
                template, temp_file = get_inv_temp(hire_inv)

        saved_docx = shutil.copy(temp_file, tempy)
        pdf_file = ot.doc.to_pdf(tempy)
        do_cmc(cmc, 'Hire', hire, tempy)
        do_email(pdf_file, ot.email)
        # opened = ot.doc.open_document(saved_docx or temp_file)
        ...



