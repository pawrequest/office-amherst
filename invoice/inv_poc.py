from docxtpl import DocxTemplate

from managers.entities import Order

doc = DocxTemplate("invoice_tmplt.docx")

line_items = [
    {'name': 'Python Books', 'qty': 2, 'price': 10},
]
order = ''


shipping = False
shipping_price = 10
goods = sum([li['qty'] * li['price'] for li in line_items])
subtotal = goods + shipping_price if shipping else goods
tax = subtotal * 0.2
total = subtotal + tax




#
# class invoice_context:
#     def __init__(self):
#         order : SaleOrder
#         inv_num = invoice_number

context = {
    'inv_num': '1234',
    'inv_date': '01.01.2017',
    'inv_address': '123 fake street'
                   '\nnot a town'
                   '\nregional'
                   '\ncounty',
    'inv_postcode': 'AB12 3CD',

    'del_address': '123 fake street'
                   '\nnot a town'
                   '\nregional'
                   '\ncounty',
    'del_postcode': 'AB12 3CD',
    'start_date': '01.01.2017',
    'due_date': '01.01.2017',
    'line_items': line_items,
    'subtotal': subtotal,
    'tax': tax,
    'total': total,
    'shipping': shipping,
    'shipping_price': shipping_price,
}
doc.render(context)
doc.save("generated_doc.docx")
