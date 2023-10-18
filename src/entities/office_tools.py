from in_out.email_funcs import GmailSender, OutlookSender
from in_out.file_management import LibreConverter, LibreHandler, WordConverter, WordHandler


class OfficeTools:
    def __init__(self, doc_handler, pdf_converter, email_sender):
        self.doc_handler = doc_handler
        self.pdf_converter = pdf_converter
        self.email_sender = email_sender


def microsoft_factory():
    return OfficeTools(WordHandler(), WordConverter(), OutlookSender())


def libre_factory():
    return OfficeTools(LibreHandler(), LibreConverter(), GmailSender())


def get_tools(use_microsoft: bool):
    return microsoft_factory() if use_microsoft else libre_factory()

# class MICROSOFT_TOOLS(OfficeTools):
#     doc_handler = WordHandler()
#     email_sender = OutlookSender()
#     pdf_converter = WordConverter()
#
#
# class LIBRE_TOOLS(OfficeTools):
#     doc_handler = LibreHandler()
#     email_sender = GmailSender()
#     pdf_converter = LibreConverter()
#
# #
# # def get_tools(use_microsoft: bool):
# #     return MICROSOFT_TOOLS if use_microsoft else LIBRE_TOOLS
#
