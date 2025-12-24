import os
import sys
import smtplib
import getpass
from dotenv import load_dotenv

load_dotenv()

from validate_email import validate_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SMTP_PORT = 25
DNI = os.getenv("DNI")
NAME = os.getenv("NAME")
SMTP_SERVER = "smtp.upv.es"
EMAIL_FROM = os.getenv("EMAIL_FROM")

EMAIL_SUBJECT = "Prac3"
EMAIL_TO = os.getenv("EMAIL_TO")
MESSAGE_BODY = f"{NAME} | {DNI}\n"
PDF_PATH = os.getenv("PDF_PATH")

msg = MIMEMultipart("mixed", "frontera")

if not validate_email(
    email_address=EMAIL_TO,
    check_format=True,
    check_blacklist=False,
    check_dns=False,
    check_smtp=False,
):
    print("Invalid email address")
    sys.exit()

msg.add_header("From", EMAIL_FROM)
msg.add_header("To", EMAIL_TO)
msg.add_header("Subject", EMAIL_SUBJECT)
text_msg = MIMEText(MESSAGE_BODY, "plain", "utf-8")
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

except:
    print("Error sending mail")
    sys.exit()

try:
    mailServer = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    # mailServer.login(user=EMAIL_FROM, password=getpass.getpass("UPV mail password: "))
    # mailServer.login(user=EMAIL_FROM, password=PASSWORD)
    mailServer.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mailServer.quit()
    print(f"Mail sent to {EMAIL_TO} from {EMAIL_FROM} with subject {EMAIL_SUBJECT}")

except smtplib.SMTPException as e:
    print(e)
    print("Error sending mail")
    sys.exit()
