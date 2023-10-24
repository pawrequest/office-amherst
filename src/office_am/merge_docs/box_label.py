from docxtpl import DocxTemplate

from office_am import dflt
from office_am.dflt import DFLT_PATHS
from office_tools.doc_handler import DocHandler

def address_rows_limited(address:str):
    add_lst = address.split('\r\n')
    if len(add_lst) > 4:
        add_lst = add_lst[:4]
    add_str = '\r\n'.join(add_lst)
    return add_str

def box_labels(hire, doc_handler: DocHandler):
    tmplt = DFLT_PATHS.BOX_TMPLT
    temp_file = dflt.DFLT_PATHS.TEMP_DOC

    del_add=address_rows_limited(hire['Delivery Address'])
    boxes = int(hire['Boxes'])
    context = dict(
                date=f"{hire['Send Out Date']:%A %d %B}",
                method=hire['Send Method'],
                customer_name=hire['To Customer'],
                delivery_address=del_add,
                delivery_contact=hire['Delivery Contact'],
                tel=hire['Delivery Tel'],
                boxes=boxes,
            )

    template = DocxTemplate(tmplt)
    template.render(context)
    template.save(temp_file)
    ...

