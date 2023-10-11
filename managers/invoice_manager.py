import datetime
from dataclasses import dataclass

from docxtpl import DocxTemplate

from managers.entities import Order

INVOICE_TMPLT = "invoice_tmplt.docx"
doc = DocxTemplate(INVOICE_TMPLT)
from decimal import Decimal


@dataclass
class Address1:
    add: str
    postcode: str


@dataclass
class HireDates:
    invoice: datetime.date
    start: datetime.date
    end: datetime.date


date_format = '%d.%m.%Y'


@dataclass()
class HireInvoice:
    inv_num: str
    dates: HireDates
    inv_add: Address1
    del_add: Address1
    inv_order: Order
    ship_price: Decimal = 13



    def get_invoice(self):
        context = {
            'inv_num': '1234',
            'dates': self.dates,
            'inv_address': self.inv_add,
            'del_address': self.del_add,
            'order': self.inv_order,
        }

        doc.render(context)
        doc.save("generated_doc.docx")
