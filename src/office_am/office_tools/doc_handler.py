import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Tuple

import PySimpleGUI as sg
from comtypes.client import CreateObject


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
