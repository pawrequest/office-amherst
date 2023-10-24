from pathlib import Path
from typing import Tuple

import PySimpleGUI as sg
from docxtpl import DocxTemplate

from office_am import dflt


def get_template_and_path(tmplt, context=None, temp_file=None) -> Tuple[DocxTemplate, Path]:
    temp_file = temp_file or dflt.DFLT_PATHS.TEMP_DOC
    context = context or dict()
    template = DocxTemplate(tmplt)
    template.render(context)

    while True:
        try:
            template.save(temp_file)
            return template, temp_file
        except Exception as e:
            if sg.popup_ok_cancel("Close the template file and try again") == 'OK':
                continue
            else:
                raise e


def try_again():
    return sg.popup_ok_cancel("Close the template file and try again")


def get_template(tmplt, temp_file, context=None) -> DocxTemplate:
    template = DocxTemplate(tmplt)

    while True:
        try:
            template.render(context)
            template.save(temp_file)
            return template
        except Exception as e:
            ans = try_again()
            if ans == 'OK':
                continue
            raise e


def templt_to_pdf(tmplt, context, doc_handler, temp_file):
    try:
        template = DocxTemplate(tmplt)
        template.render(context)
        template.save(temp_file)
        pdf_file = doc_handler.to_pdf(temp_file)
    except Exception as e:
        ...
    else:
        return pdf_file
