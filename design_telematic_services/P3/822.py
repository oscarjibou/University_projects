from validate_email import validate_email
from textwrap import TextWrapper

# Importamos los módulos que necesitamos de la librería email
from email.message import EmailMessage

# Importamos la librería smtplib
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

email_from = os.getenv("EMAIL_FROM")

"""
This script sends an email using the SMTP protocol. It performs the following steps:
1. Imports necessary libraries and modules.
2. Creates an EmailMessage object.
3. Prompts the user to input the recipient's email address and validates it.
4. Prompts the user to input the email subject.
5. Prompts the user to input the email body, allowing multiple lines and wrapping lines longer than 78 characters.
6. Sends the email using the SMTP server of UPV.

Functions:
- validate_email: Validates the format of the recipient's email address.
- TextWrapper: Wraps text to a specified width.
- EmailMessage: Creates an email message object.
- smtplib.SMTP: Establishes a connection to the SMTP server and sends the email.

Variables:
- email_from: Sender's email address.
- email_to: Recipient's email address.
- es_valido: Boolean indicating whether the recipient's email address is valid.
- msg: EmailMessage object containing the email headers and body.
- contents: List of strings representing the lines of the email body.
- wrapper: TextWrapper object for wrapping lines of text.
- body: String containing the complete email body.
- mailServer: SMTP object for sending the email.

Exceptions:
- smtplib.SMTPException: Catches and prints any SMTP-related errors that occur during the sending process.
"""

# Creamos el objeto de la clase EmailMessage
msg = EmailMessage()

# Cabecera
email_to = input("Destinatario: ")

es_valido = validate_email(
    email_address=email_to,
    check_format=True,
    check_blacklist=False,
    check_dns=False,
    check_smtp=False,
)
while es_valido == False:
    # La dirección de correo es incorrecta
    print("Dirección Incorrecta. Introduzca la dirección de destino de nuevo.")
    email_to = input("Destinatario: ")
    es_valido = validate_email(
        email_address=email_to,
        check_format=True,
        check_blacklist=False,
        check_dns=False,
        check_smtp=False,
    )
msg.add_header("From", email_from)
msg.add_header("To", email_to)
msg.add_header("Subject", input("Asunto:"))

# Cuerpo del mensaje
print(
    'Introduzca el contenido del mensaje por ahora solo US-ASCII. Finalice con un "." en una línea vacía'
)
contents = []
wrapper = TextWrapper(width=78)
while True:
    line = input()
    if line == ".":
        break
    # Ajustamos las líneas con tamaño máximo 78 caracteres
    if len(line) <= 78:
        contents.append(line)
    else:
        lineas = wrapper.wrap(text=line)
        for i in lineas:
            contents.append(i)
# Creamos el cuerpo del mensaje
body = "\n".join(contents)
msg.set_content(body)
# Enviamos el correo electrónico utilizando el protocolo SMTP
try:
    # Establecemos la conexion con el servidor smtp de la UPV
    mailServer = smtplib.SMTP("smtp.upv.es", 25)
    # Enviamos el mensaje
    mailServer.sendmail(email_from, email_to, msg.as_string())
    # Cierre de la conexión
    mailServer.quit()
    print("Correo electrónico enviado")
except smtplib.SMTPException as e:
    print("Se ha producido un error STMP: " + str(e))
    print("Correo electrónico no enviado")
