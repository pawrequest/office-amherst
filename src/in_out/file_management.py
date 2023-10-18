import PySimpleGUI as sg
import asyncio
import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Tuple

from comtypes.client import CreateObject
from docx2pdf import convert as convert_word



# convert doc to pdf
class PDFConverter(ABC):
    @abstractmethod
    def from_docx(self, out_file: Path):
        raise NotImplementedError


class WordConverter(PDFConverter):
    def from_docx(self, doc_file: Path):
        try:
            convert_word(doc_file, output_path=doc_file.parent, keep_active=True)
            outfile = doc_file.with_suffix('.pdf')
            print(f"Converted {outfile}")
            return outfile
        except Exception as e:
            raise e


class LibreConverter(PDFConverter):
    def from_docx(self, doc_file: Path):
        try:
            subprocess.run(f'soffice --headless --convert-to pdf {str(doc_file)} --outdir {str(doc_file.parent)}')
            outfile = doc_file.with_suffix('.pdf')
            print(f"Converted {outfile}")
            return outfile
        except Exception as e:
            ...


# open doc

class DocHandler(ABC):
    @abstractmethod
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        raise NotImplementedError

    def save_document(self, doc, out_file: Path):
        if out_file.exists():
            if sg.popup_ok_cancel(f'{out_file} already exists, overwrite?') != 'OK':
                raise FileExistsError(f"File already exists: {out_file}")
        shutil.copy(doc, out_file)
        print(f"Saved {out_file}")
        return out_file


class WordHandler(DocHandler):
    # todo use library
    def open_document(self, doc_path: Path) -> Tuple:
        try:
            word = CreateObject('Word.Application')
            word.Visible = True
            word_doc: word.Document = word.Documents.Open(str(doc_path))
            return word, word_doc
        except OSError as e:
            print(f"Is Word installed? Failed to open {doc_path} with error: {e}")
            raise e
        except Exception as e:
            raise e


class LibreHandler(DocHandler):
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        try:
            process = subprocess.Popen(['soffice', str(doc_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            raise e
        return process, None


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

