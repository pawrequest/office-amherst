from in_out.email_funcs import EmailSender, GmailSender, OutlookSender
from in_out.file_management import DocHandler, LibreConverter, LibreHandler, PdfConverter, WordConverter, WordHandler


class MICROSOFT_TOOLS:
    doc_handler = WordHandler()
    email_sender = OutlookSender()
    pdf_converter = WordConverter()

class LIBRE_TOOLS:
    doc_handler = LibreHandler()
    email_sender = GmailSender()
    pdf_converter = LibreConverter()


def get_tools(use_microsoft: bool):
    if use_microsoft:
        return MICROSOFT_TOOLS.doc_handler, MICROSOFT_TOOLS.email_sender, MICROSOFT_TOOLS.pdf_converter
    else:
        return LIBRE_TOOLS.doc_handler, LIBRE_TOOLS.email_sender, LIBRE_TOOLS.pdf_converter



class OfficeTools:
    def __init__(self, doc_handler, pdf_converter, email_sender):
        self.doc_handler = doc_handler
        self.pdf_converter = pdf_converter
        self.email_sender = email_sender

    @classmethod
    def get_tools(cls, use_microsoft: bool):
        if use_microsoft:
            return MICROSOFT_TOOLS.doc_handler, MICROSOFT_TOOLS.pdf_converter, MICROSOFT_TOOLS.email_sender
        else:
            return LIBRE_TOOLS.doc_handler, LIBRE_TOOLS.pdf_converter, LIBRE_TOOLS.email_sender
