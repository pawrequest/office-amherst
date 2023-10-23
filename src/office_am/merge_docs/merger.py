from pathlib import Path
from typing import Tuple

import PySimpleGUI as sg
from docxtpl import DocxTemplate
from office_am import dflt


def get_template_and_path(tmplt, context = None, temp_file = None) -> Tuple[DocxTemplate, Path]:
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


context = dict(
    date = 'adate',
    deliver_to = 'delvierto',
    foa = 'foa',
    tel = 'tel',
    packages = 'packages',
)



# templat, tempfile = get_template_and_path(tmplt = dflt.DFLT_PATHS.BOX_TMPLT, context=context)
...
