import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from docx2pdf import convert as convert_word


class PDFConverter(ABC):
    @abstractmethod
    def from_docx(self, out_file: Path) -> Path:
        raise NotImplementedError


class LibreConverter(PDFConverter):
    def from_docx(self, doc_file: Path) -> Path:
        try:
            subprocess.run(f'soffice --headless --convert-to pdf {str(doc_file)} --outdir {str(doc_file.parent)}')
            outfile = doc_file.with_suffix('.pdf')
            print(f"Converted {outfile}")
            return outfile
        except FileNotFoundError as e:
            print('Is LibreOffice installed?')
        except Exception as e:
            ...


class WordConverter(PDFConverter):
    def from_docx(self, doc_file: Path) -> Path:
        try:
            convert_word(doc_file, output_path=doc_file.parent, keep_active=True)
            outfile = doc_file.with_suffix('.pdf')
            print(f"Converted {outfile}")
            return outfile
        except Exception as e:
            raise e
