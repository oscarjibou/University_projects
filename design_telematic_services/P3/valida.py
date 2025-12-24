from validate_email import validate_email
import os
from dotenv import load_dotenv
load_dotenv()
"""
This script validates an email address entered by the user.

Modules:
    validate_email: A module to validate email addresses.

Variables:
    email_from (str): A sample email address.
    email_to (str): The email address entered by the user.
    es_valido (bool): A flag indicating whether the entered email address is valid.

Functions:
    validate_email: Validates the email address based on the specified criteria.

Usage:
    Run the script and enter an email address when prompted. The script will check if the email address is valid based on the format. If the email address is invalid, the user will be prompted to enter the email address again until a valid one is provided.
"""

email_from = os.getenv("EMAIL_FROM")
print("Introduzca un email para comprobar si es correcto")
email_to = input("Destinatario:")
es_valido = validate_email(
    email_address=email_to,
    check_format=True,
    check_blacklist=False,
    check_dns=False,
    check_smtp=False,
)
while es_valido == False:
    # La dirección de correo es incorrecta
    print("Dirección Incorrecta.Introduzca la dirección de destino de nuevo.")
    email_to = input("Destinatario:")
    es_valido = validate_email(
        email_address=email_to,
        check_format=True,
        check_blacklist=False,
        check_dns=False,
        check_smtp=False,
    )

# varios ejemplos de direcciones de correo electrónico (algunos erróneos) para probar la función
examples_error = [
    "plainaddress",
    "@missingusername.com",
    "username@.com",
    "username@.com.",
    "username@missingdotcom",
    "username@missingtld.",
    "username@-domain.com",
    "username@domain..com",
]

examples_correct = [
    "username@example.com",
    "user.name+tag+sorting@example.com",
    "user.name@example.co.uk",
    "user_name@example.com",
    "username@subdomain.example.com",
    "username@domain.com",
    "username@domain.co.in",
    "username@domain.io",
]
