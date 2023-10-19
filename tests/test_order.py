import tempfile
from pathlib import Path

from office_am.dflt import DFLT_PATHS
from office_am.main import do_all
from office_am.office_tools.o_tool import OfficeTools
from office_am.order.invoice import get_inv_temp
from office_am.order.order_ent import LineItem
from office_am.order.transact import TransactionContext
from office_am.cmc.commence import CmcContext
from office_am.office_tools import o_tool



def test_libre():
    with CmcContext() as cmc:
        temp_dir = tempfile.mkdtemp()
        outfile = Path(temp_dir) / "outfile.docx"
        ot = OfficeTools.libre()

        hires = cmc.hires_by_customer('Test')
        hire= hires[0]
        with TransactionContext() as tm:
            hire_inv = tm.get_hire_invoice(hire)
            assert isinstance(hire_inv.order.line_items[0], LineItem)
            out_file = (DFLT_PATHS.INV_OUT_DIR / hire_inv.inv_num).with_suffix('.docx')
            template, temp_file_ = get_inv_temp(hire_inv)

            saved_docx = ot.doc.save_document(temp_file_, outfile)
            pdf_file = ot.pdf.from_docx(outfile)
            assert pdf_file.is_file()
            # print_file(outfile.with_suffix('.pdf'))
            # do_cmc(cmc, 'Hire', hire, outfile)
            # do_email(pdf_file, ot)
            # opened = ot.doc.open_document(saved_docx or temp_file)

        ...
