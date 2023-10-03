from dbfread import DBF

from docxtpl import DocxTemplate


def main():
    hire = [i for i in DBF('../fixtures/hire_sheet.dbf', load=True, encoding='cp1251')][0]

    hire_template = r'C:\paul\office_am\fixtures\hire_sheet_tmplt.docx'
    context = {k: v for k, v in hire.items()}
    for k, v in context.items():
        if isinstance(v, str):
            context[k] = v.split('\x00')[0]

    doc = DocxTemplate(hire_template)
    doc.render(context)
    doc.save("generated_doc.docx")


if __name__ == '__main__':
    main()
