import pyotp
import base64
from dotenv import load_dotenv
import os
load_dotenv()

dni = os.getenv("DNI")
secret = base64.b32encode(bytearray(dni, "ascii")).decode("utf-8")
print("mi secreto:", secret)
totp_object = pyotp.TOTP(secret)
qr_text = totp_object.provisioning_uri(name="mi_usuario", issuer_name="Mi App")
print(qr_text)

otp = input("ingresa el código OTP:")
valid = totp_object.verify(otp)
print(valid)
