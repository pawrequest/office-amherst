# import webbrowser
# from pathlib import Path
#
# from win32com.client import Dispatch
# class EmailSendingProtocol(Protocol):
#     def send_email(self, email: 'Email') -> None:
#         ...
#
# class Email:
#     def __init__(self, to_address: str, subject: str, body: str, attachment_path: Path = None):
#         self.attachment_path = attachment_path
#         self.to_address = to_address
#         self.subject = subject
#         self.body = body
# #
#
# def gmail_compose_link(email: Email) -> str:
#     to_encoded = email.to_address.replace('@', '%40')
#     subject_encoded = email.subject.replace(' ', '%20')
#     body_encoded = email.body.replace(' ', '%20')
#     attachment_param = ""
#     if email.attachment_path:
#         attachment_param = f"&attfi={str(email.attachment_path)}"
#     compose_link = f"https://mail.google.com/mail/u/0/?view=cm&fs=1&to={to_encoded}&su={subject_encoded}&body={body_encoded}{attachment_param}"
#     return compose_link
#
# def send_outlook(email:Email):
#     outlook = Dispatch('outlook.application')
#     mail = outlook.CreateItem(0)
#     mail.To = 'admin@amherst.co.uk'  # replace with recipient's email
#     mail.Subject = 'Invoice Attached'
#     mail.Body = 'Please find the attached invoice.'
#     mail.Attachments.Add(str(email.attachment_path))
#     mail.Display(True)
#     # mail.Send()
#
#
#


import webbrowser
from abc import ABC
from pathlib import Path
from typing import Optional

from win32com.client import Dispatch
from win32com.universal import com_error


class EmailSender(ABC):
    def send_email(self, email: 'Email') -> None:
        ...


class Email:
    def __init__(self, to_address: str, subject: str, body: str, attachment_path: Optional[Path] = None):
        self.attachment_path = attachment_path
        self.to_address = to_address
        self.subject = subject
        self.body = body

    def send(self, sender: EmailSender) -> None:
        sender.send_email(self)


class OutlookSender(EmailSender):
    def send_email(self, email: Email) -> bool:
        try:
            outlook = Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = email.to_address
            mail.Subject = email.subject
            mail.Body = email.body
            if email.attachment_path:
                mail.Attachments.Add(str(email.attachment_path))
            mail.Display(True)
            # mail.Send()
            return True
        except com_error as e:
            msg = f"Outlook not installed - {e.args[0]}"
            print(msg)
            raise EmailError(msg)
        except Exception as e:
            msg = f"Failed to send email with error: {e.args[0]}"
            print(msg)
            raise EmailError(msg)


class EmailError(Exception):
    ...


class GmailSender(EmailSender):
    def send_email(self, email: Email) -> None:
        compose_link = gmail_compose_link(email)
        webbrowser.open(compose_link)


def gmail_compose_link(email: Email) -> str:
    to_encoded = email.to_address.replace('@', '%40')
    subject_encoded = email.subject.replace(' ', '%20')
    body_encoded = email.body.replace(' ', '%20')
    compose_link = f"https://mail.google.com/mail/u/0/?view=cm&fs=1&to={to_encoded}&su={subject_encoded}&body={body_encoded}"
    return compose_link


