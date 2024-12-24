import base64
import pyotp
import socket

DNI = "44895422"
NAME = "Oscar Jimenez Bou"
IP_ADDRESS = "158.42.32.220"
PORT = 21000

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((IP_ADDRESS, PORT))

otp = pyotp.TOTP(base64.b32encode(DNI.encode()).decode()).now()
print("OTP:", otp)

message = f"{NAME}&{DNI}&{otp}"
print("Message:", message)

socket.send(message.encode())
response = socket.recv(1024)
print(f"Server response: {response.decode()}")

socket.close()
