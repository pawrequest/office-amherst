from ..office_tools.email_handler import EmailSender, OutlookSender, GmailSender
from .pdf_handler import LibreConverter, PDFConverter, WordConverter
from .doc_handler import DocHandler, LibreHandler, WordHandler


class OfficeTools:
    def __init__(self, doc:DocHandler, pdf:PDFConverter, email:EmailSender):
        self.doc = doc
        self.pdf = pdf
        self.email = email

    @classmethod
    def microsoft(cls) -> 'OfficeTools':
        return cls(WordHandler(), WordConverter(), OutlookSender())
    @classmethod
    def libre(cls) -> 'OfficeTools':
        return cls(LibreHandler(), LibreConverter(), GmailSender())

