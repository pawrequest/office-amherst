from entities.dflt import USE_MICROSOFT
from in_out.email_funcs import GmailSender, OutlookSender
from in_out.file_management import LibreConverter, LibreHandler, WordConverter, WordHandler


class MICROSOFT_TOOLS:
    DOC_HANDLER = WordHandler()
    EMAIL_SENDER = OutlookSender()
    PDF_CONVERTER = WordConverter()


class LIBRE_TOOLS:
    DOC_HANDLER = LibreHandler()
    EMAIL_SENDER = GmailSender()
    PDF_CONVERTER = LibreConverter()


def get_tools():
    if USE_MICROSOFT:
        return MICROSOFT_TOOLS.DOC_HANDLER, MICROSOFT_TOOLS.EMAIL_SENDER, MICROSOFT_TOOLS.PDF_CONVERTER
    else:
        return LIBRE_TOOLS.DOC_HANDLER, LIBRE_TOOLS.EMAIL_SENDER, LIBRE_TOOLS.PDF_CONVERTER
