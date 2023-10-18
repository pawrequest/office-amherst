from in_out.email_funcs import EmailSender, GmailSender, OutlookSender
from in_out.file_management import DocHandler, LibreConverter, LibreHandler, PdfConverter, WordConverter, WordHandler


class MICROSOFT_TOOLS:
    DOC_HANDLER = WordHandler()
    EMAIL_SENDER = OutlookSender()
    PDF_CONVERTER = WordConverter()

MIC_TOOLS = dict(
    DOC_HANDLER=WordHandler(),
    PDF_CONVERTER=WordConverter(),
    EMAIL_SENDER=OutlookSender(),
)

LIB_TOOLS = dict(
    DOC_HANDLER=LibreHandler(),
    PDF_CONVERTER=LibreConverter(),
    EMAIL_SENDER=GmailSender(),
)

class LIBRE_TOOLS:
    DOC_HANDLER = LibreHandler()
    EMAIL_SENDER = GmailSender()
    PDF_CONVERTER = LibreConverter()


def get_tools(use_microsoft: bool):
    if use_microsoft:
        return MICROSOFT_TOOLS.DOC_HANDLER, MICROSOFT_TOOLS.EMAIL_SENDER, MICROSOFT_TOOLS.PDF_CONVERTER
    else:
        return LIBRE_TOOLS.DOC_HANDLER, LIBRE_TOOLS.EMAIL_SENDER, LIBRE_TOOLS.PDF_CONVERTER



class OfficeTools:
    def __init__(self, doc_handler, pdf_converter, email_sender):
        self.doc_handler = doc_handler
        self.pdf_converter = pdf_converter
        self.email_sender = email_sender

    @classmethod
    def get_tools(cls, use_microsoft: bool):
        if use_microsoft:
            return cls(*MIC_TOOLS)
        else:
            return cls(*LIB_TOOLS)
