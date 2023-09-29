from docxtpl import DocxTemplate

doc = DocxTemplate("invoice_tmplt.docx")

line_items = [
    {'id': 1, 'name': 'Python Books', 'qty': 2, 'price': 10},
    {'id': 2, 'name': 'Django Books', 'qty': 2, 'price': 10},
    {'id': 3, 'name': 'Flask Books', 'qty': 2, 'price': 10},
]

shipping = False
shipping_price = 10
goods = sum([li['qty'] * li['price'] for li in line_items])
subtotal = goods + shipping_price if shipping else goods
tax = subtotal * 0.2
total = subtotal + tax

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
