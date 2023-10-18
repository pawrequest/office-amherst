from in_out.email_funcs import EmailSender, OutlookSender, GmailSender
from in_out.file_management import DocHandler, PDFConverter, WordHandler, WordConverter, LibreConverter, LibreHandler


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

