import argparse
import os

from dbfread import DBF
from docxtpl import DocxTemplate


def amherst_doc(dbf, template, output, customer_data=None):
    input_record = [i for i in DBF(dbf, load=True, encoding='cp1251')][0]

    context = {k: v for k, v in input_record.items()}

    if customer_data is not None:
        with open(customer_data, 'r') as f:
            cust_data = f.read()
        context['c_data'] = cust_data
    for k, v in context.items():
        if isinstance(v, str):
            context[k] = v.split('\x00')[0]

    doc = DocxTemplate(template)
    doc.render(context)

    doc.save(output)
    # os.startfile(str(output), "print")
    os.startfile(str(output))


def main():
    parser = argparse.ArgumentParser(description='Generate Amherst Doc')
    parser.add_argument('--template', help='Path to template file')
    parser.add_argument('--dbf', help='Path to DBF file')
    parser.add_argument('--output', help='Path to output file')
    parser.add_argument('--customer_data', default=None, help='Path to output file')

    args = parser.parse_args()
    amherst_doc(template=args.template, dbf=args.dbf, output=args.output, customer_data=args.customer_data)


if __name__ == '__main__':
    main()

def hire_sheet_aget():
    return r'C:\paul\office_am\venv\Scripts\python.exe C:\paul\office_am\word\doc_templater.py --dbf ''C:\paul\office_am\input_files\hire_sheet.dbf ' r'--template C:\paul\office_am\tmplt\hire_sheet_tmplt.docx --output C:\paul\office_am\generated_docs\hire_sheet_output.docx'
