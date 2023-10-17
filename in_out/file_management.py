import os
import subprocess
from pathlib import Path

from docx2pdf import convert as convert_word
from win32com.client import Dispatch


def pdf_convert(out_file: Path):
    try:
        convert_word(out_file, keep_active=True)
    except Exception as e:
        convert_pdf_libreoffice(docx_file=out_file)
    finally:
        print(f"Converted {out_file}")


def convert_pdf_libreoffice(docx_file: Path):
    out_dir = docx_file.parent
    subprocess.run(f'soffice --headless --convert-to pdf {str(docx_file)} --outdir {str(out_dir)}')


def print_file(file_path: Path):
    try:
        os.startfile(str(file_path), "print")
        return True
    except Exception as e:
        print(f"Failed to print: {e}")
        return False


def send_email(attachment_path):
    outlook = Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'admin@amherst.co.uk'  # replace with recipient's email
    mail.Subject = 'Invoice Attached'
    mail.Body = 'Please find the attached invoice.'
    mail.Attachments.Add(str(attachment_path))
    mail.Display(True)
    # mail.Send()
