import shutil
import winreg as reg
from functools import lru_cache

from .doc_handler import DocHandler, LibreHandler, WordHandler
from .pdf_handler import LibreConverter, PDFConverter, WordConverter
from ..office_tools.email_handler import EmailHandler, GmailSender, OutlookSender


class OfficeTools:
    def __init__(self, doc: DocHandler, pdf: PDFConverter, email: EmailHandler):
        self.doc = doc
        self.pdf = pdf
        self.email = email

    @classmethod
    def microsoft(cls) -> 'OfficeTools':
        return cls(WordHandler(), WordConverter(), OutlookSender())

    @classmethod
    def libre(cls) -> 'OfficeTools':
        return cls(LibreHandler(), LibreConverter(), GmailSender())

    @classmethod
    def auto_select(cls) -> 'OfficeTools':

        if not cls._something_installed():
            raise EnvironmentError("Neither Microsoft nor LibreOffice tools are installed")
        tools_status = cls._get_tools_status()

        word_handler = WordHandler if tools_status['word'] else LibreHandler
        pdf_converter = WordConverter if tools_status[
            'excel'] else LibreConverter  # Assuming Excel is used for PDF conversion
        email_handler = OutlookSender if tools_status['outlook'] else GmailSender

        return cls(word_handler(), pdf_converter(), email_handler())

    @classmethod
    @lru_cache(maxsize=None)  # Unbounded cache
    def _get_tools_status(cls) -> dict:
        tools_status = {
            'word': cls._check_registry(r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\WINWORD.EXE"),
            'excel': cls._check_registry(r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\EXCEL.EXE"),
            'outlook': cls._check_registry(r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\OUTLOOK.EXE"),
            'libre': cls._check_soffice_path()
        }
        return tools_status

    @classmethod
    def _something_installed(cls) -> bool:
        stat = cls._get_tools_status()
        doc = any([stat['word'], stat['libre']])
        sheet = any([stat['excel'], stat['libre']])
        return all([doc, sheet])

    @staticmethod
    @lru_cache(maxsize=None)  # Unbounded cache
    def _check_registry(reg_path: str) -> bool:
        try:
            key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path)
            reg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False

    @staticmethod
    @lru_cache(maxsize=None)  # Unbounded cache
    def _check_soffice_path() -> bool:
        return shutil.which("soffice.exe") is not None
