import datetime
from dataclasses import dataclass

from docxtpl import DocxTemplate

from managers.entities import Order, DFLT
from decimal import Decimal

INVOICE_TMPLT = DFLT.INV_TMPLT
doc = DocxTemplate(INVOICE_TMPLT)


@dataclass
class Address1:
    add: str
    pc: str


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

    @classmethod
    def from_hire(cls, hire, order):
        i_add = hire['Delivery Address']
        i_pc = hire['Delivery Postcode']
        d_add = hire['Delivery Address']
        d_pc = hire['Delivery Postcode']
        inv_add = Address1(add=i_add, pc=i_pc)
        del_add = Address1(add=d_add, pc=d_pc)
        date_inv = hire['Booked Date']
        date_start = hire['Send Out Date']
        date_end = hire['Due Back Date']
        dates = HireDates(invoice=date_inv, start=date_start, end=date_end)
        return cls(inv_num='1234', dates=dates, inv_add=inv_add, del_add=del_add, inv_order=order)



    def generate(self):
        context = {
            'inv_num': '1234',
            'dates': self.dates,
            'inv_address': self.inv_add,
            'del_address': self.del_add,
            'order': self.inv_order,
        }

        doc.render(context)
        ...
        doc.save(DFLT.INV_OUT)


