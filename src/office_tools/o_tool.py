import itertools
import shutil
from functools import lru_cache

from .doc_handler import DocHandler, LibreHandler, WordHandler
from .email_handler import EmailHandler, GmailSender, OutlookSender
from .system_tools import check_registry


class OfficeTools:
    def __init__(self, doc: DocHandler, email: EmailHandler):
        self.doc = doc
        self.email = email

    @classmethod
    def microsoft(cls) -> 'OfficeTools':
        return cls(WordHandler(), OutlookSender())

    @classmethod
    def libre(cls) -> 'OfficeTools':
        return cls(LibreHandler(), GmailSender())

    @classmethod
    def auto_select(cls) -> 'OfficeTools':
        if not tools_available():
            raise EnvironmentError("Neither Microsoft nor LibreOffice tools are installed")

        doc_handler = WordHandler if check_word() else LibreHandler
        email_handler = OutlookSender if check_outlook() else GmailSender

        return cls(doc_handler(), email_handler())


def tools_available() -> bool:
    """ Check if either Microsoft or LibreOffice tools for docs and sheets are installed"""
    libre = check_libre()
    word = check_word()
    excel = check_excel()
    return all([(word or libre), (excel or libre)])


@lru_cache(maxsize=None)
def check_word() -> bool:
    return check_registry(r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\WINWORD.EXE")


@lru_cache(maxsize=None)
def check_excel() -> bool:
    return check_registry(r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\EXCEL.EXE")


@lru_cache(maxsize=None)
def check_outlook() -> bool:
    return check_registry(r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\OUTLOOK.EXE")


@lru_cache(maxsize=None)
def check_libre() -> bool:
    return shutil.which("soffice.exe") is not None


def get_installed_combinations():
    doc_handlers = []
    email_handlers = []

    if check_word():
        doc_handlers.append(WordHandler)
    if check_libre():
        doc_handlers.append(LibreHandler)

    if check_outlook():
        email_handlers.append(OutlookSender)

    email_handlers.append(GmailSender)

    for doc_handler, email_handler in itertools.product(doc_handlers, email_handlers):
        yield OfficeTools(doc_handler(), email_handler())
