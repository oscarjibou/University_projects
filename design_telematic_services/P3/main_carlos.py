import os
import sys
import smtplib

from validate_email import validate_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

DNI = os.getenv("DNI")
PDF_PATH = os.getenv("PDF_PATH")

SMTP_SERVER = "smtp.upv.es"
SMTP_PORT = 25

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO_ = os.getenv("EMAIL_TO_")
EMAIL_SUBJECT = "Prac3"
EMAIL_MESSAGE = f"Mi nombre es: {NAME} \n Mi DNI es: {DNI}"


def validate_email_custom(email):
    """
    Custom email validation function
    """
    if not validate_email(
        email_address=email,
        check_format=True,
        check_blacklist=True,
        check_dns=False,
        check_smtp=False,
    ):
        print("El email no es valido")
        exit(1)
    else:
        print("El email es valido")


validate_email_custom(EMAIL_TO_)
msg = MIMEMultipart("mixed", "frontera")
msg.add_header("From", EMAIL_FROM)
msg.add_header("To", EMAIL_TO_)
msg.add_header("Subject", EMAIL_SUBJECT)
text_msg = MIMEText(EMAIL_MESSAGE, "plain", "utf-8")
msg.attach(text_msg)

try:
    file = open(PDF_PATH, "rb")
    document = MIMEApplication(file.read(), "pdf")
    document.add_header(
        "ContentDisposition", 'attachment; filename = "' + PDF_PATH + '"'
    )
    msg.attach(document)
    file.close()
except OSError as e:
    print(e)
    print("Error sending mail")
    sys.exit()


try:
    mailServer = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.sendmail(EMAIL_FROM, EMAIL_TO_, msg.as_string())
    mailServer.quit()
    print(f"Mail sent to {EMAIL_TO_} from {EMAIL_FROM} with subject {EMAIL_SUBJECT}")
except smtplib.SMTPException as e:
    print(e)
    print("Error sending mail")
    sys.exit()
