import argparse
import os

from dbfread import DBF

from docxtpl import DocxTemplate

HIRE_TEMPLATE = r'C:\paul\office_am\fixtures\hire_sheet_tmplt.docx'
HIRE_DBF_EXAMPLE = r'C:\paul\office_am\fixtures\hire_sheet.dbf'
HIRE_SHEET_OUTPUT = r'C:\paul\office_am\fixtures\hire_sheet_output2.docx'
def amherst_doc(template = HIRE_TEMPLATE, dbf= HIRE_DBF_EXAMPLE, output=HIRE_SHEET_OUTPUT):
    hire = [i for i in DBF(dbf, load=True, encoding='cp1251')][0]

    context = {k: v for k, v in hire.items()}
    for k, v in context.items():
        if isinstance(v, str):
            context[k] = v.split('\x00')[0]

    doc = DocxTemplate(template)
    doc.render(context)

    doc.save(output)
    os.startfile(str(output), "print")


def main():
    parser = argparse.ArgumentParser(description='Generate Amherst Doc')
    parser.add_argument('--template', default=HIRE_TEMPLATE, help='Path to template file')
    parser.add_argument('--dbf', default=HIRE_DBF_EXAMPLE, help='Path to DBF file')
    parser.add_argument('--output', default=HIRE_SHEET_OUTPUT, help='Path to output file')

    args = parser.parse_args()
    amherst_doc(args.template, args.dbf, args.output)

if __name__ == '__main__':
    main()