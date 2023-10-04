from docxtpl import DocxTemplate

from invoice.products import get_all_sale_products, line_items_from_hire
from word.dde import get_hire_data_inv

doc = DocxTemplate(r"C:\paul\office_am\tmplt\hire_inv_tmplt.docx")

def hire_invoice(hire_name):
    hire_data = get_hire_data_inv(hire_name)
    products = get_all_sale_products('C:\paul\office_am\input_files\prices.xlsx', 'Hire')
    li = line_items_from_hire(products, hire_data)
    return hire_data, li


def product_names_from_hire(hire_data):
    product_names = []
    for k, v in hire_data['data'].items():
        if k.startswith('Number'):
            product_name = k.split('Number ')[1]
            product_names.append(product_name)
    return product_names

iv = hire_invoice('Test - 16/08/2023 ref 31619')
...
#
# hire_data = get_hire_data_inv('Test - 16/08/2023 ref 31619')
# li = get_line_items(hire_data)

# hi = hire_invoice('Test - 16/08/2023 ref 31619')

# inv_address = f"{hi['data']['Delivery Name']}\n{hi['data']['Delivery Address']}\n{hi['data']['Delivery Postcode']}"
