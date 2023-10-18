import shutil

import PySimpleGUI as sg
import asyncio
import os
import subprocess
from pathlib import Path
from typing import Any, Optional, Protocol, Tuple
from entities.dflt import DFLT_PATHS
from comtypes.client import CreateObject
from docx2pdf import convert as convert_word


# convert doc to pdf
class PdfConverter(Protocol):
    def convert(self, out_file: Path):
        ...


class WordConverter:
    def convert(self, doc_file: Path):
        try:
            convert_word(doc_file, output_path=doc_file.parent, keep_active=True)
            outfile= doc_file.with_suffix('.pdf')
            print(f"Converted {outfile}")
            return outfile
        except Exception as e:
            raise e


class LibreConverter:
    def convert(self, doc_file: Path):
        try:
            subprocess.run(f'soffice --headless --convert-to pdf {str(doc_file)} --outdir {str(doc_file.parent)}')
            outfile = doc_file.with_suffix('.pdf')
            print(f"Converted {outfile}")
            return outfile
        except Exception as e:
            ...


# open doc

class DocHandler(Protocol):
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        ...
    def save_document(self):
        ...


class WordHandler:
    # todo use library
    def open_document(self, doc_path: Path) -> Tuple:
        try:
            word = CreateObject('Word.Application')
            word.Visible = True
            word_doc:word.Document = word.Documents.Open(str(doc_path))
            return word, word_doc
        except Exception as e:
            raise e

    def save_document(self, word_doc, out_file: Path, keep_open: bool = False):
        if out_file.exists():
            raise FileExistsError(f"File already exists: {out_file}")
        word_doc.SaveAs(out_file)
        print(f"Saved {out_file}")
        if not keep_open:
            word_doc.Close()


class LibreHandler:
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        return None, None
    def save_document(self, doc: Path, out_file: Path, keep_open: bool = False):
        if out_file.exists():
            raise FileExistsError(f"File already exists: {out_file}")
        shutil.copy(doc, out_file)
        print(f"Saved {out_file}")
        if keep_open:
            try:
                process = subprocess.Popen(['soffice', str(out_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                raise e
def print_file(file_path: Path):
    try:
        os.startfile(str(file_path), "print")
        return True
    except Exception as e:
        print(f"Failed to print: {e}")
        return False




async def wait_for_process(process):
    while True:
        res = process.poll()
        if res is not None:
            break
        await asyncio.sleep(3)
    print("Process has finished.")
