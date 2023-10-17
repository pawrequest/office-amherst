import os
import subprocess
from pathlib import Path
from docx2pdf import convert as convert_word
from typing import Protocol

class PdfConverter(Protocol):
    def convert(self, out_file: Path):
        ...


class WordConverter:
    def convert(self, out_file: Path):
        try:
            convert_word(out_file, keep_active=True)
        except Exception as e:
            convert_pdf_libreoffice(docx_file=out_file)
        finally:
            print(f"Converted {out_file}")

class LibreConverter:
    def convert(self, out_file: Path):
        try:
            subprocess.run(f'soffice --headless --convert-to pdf {str(out_file)} --outdir {str(out_file.parent)}')
            return True
        except Exception as e:
            ...
        finally:
            print(f"Converted {out_file}")


def pdf_convert(out_file: Path):
    try:
        convert_word(out_file, keep_active=True)
    except Exception as e:
        convert_pdf_libreoffice(docx_file=out_file)
    finally:
        print(f"Converted {out_file}")


def convert_pdf_libreoffice(docx_file: Path):
    out_dir = docx_file.parent
    subprocess.run(f'soffice --headless --convert-to pdf {str(docx_file)} --outdir {str(out_dir)}')


def print_file(file_path: Path):
    try:
        os.startfile(str(file_path), "print")
        return True
    except Exception as e:
        print(f"Failed to print: {e}")
        return False


from typing import Protocol, Tuple, Any
from pathlib import Path
from comtypes.client import CreateObject


class DocumentOpenerProtocol(Protocol):
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        ...


class WordOpener:
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        try:
            word = CreateObject('Word.Application')
            word.Visible = True
            word_doc = word.Documents.Open(str(doc_path))
            return word, word_doc
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None


class LibreOpener:
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        try:
            process = subprocess.Popen(['soffice', str(doc_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return process, None  # Returning None as the second element as LibreOffice doesn't provide a document object
        except Exception as e:
            raise e

