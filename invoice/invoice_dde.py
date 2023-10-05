from pathlib import Path

from docxtpl import DocxTemplate

from invoice.products import get_all_sale_products, get_all_hire_products
from tmplt.entities import PRICES_WB, templates

doc = DocxTemplate(templates / 'invoice_tmplt.docx')
...
SALES_PRODUCTS = get_all_sale_products(PRICES_WB)
HIRE_PRODUCTS = get_all_hire_products(PRICES_WB)

...



# def hire_invoice(hire_name):
#     hire_data = get_hire_data_inv(hire_name)
#     li = line_items_from_hire(products, hire_data)
#     return hire_data, li


# iv = hire_invoice('Test - 16/08/2023 ref 31619')
# ...
#
# hire_data = get_hire_data_inv('Test - 16/08/2023 ref 31619')
# li = get_line_items(hire_data)

# hi = hire_invoice('Test - 16/08/2023 ref 31619')

# inv_address = f"{hi['data']['Delivery Name']}\n{hi['data']['Delivery Address']}\n{hi['data']['Delivery Postcode']}"
