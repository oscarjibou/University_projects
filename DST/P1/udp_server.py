import socket

UDP_address = "127.0.0.1"
UDP_port = 16000
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_address, UDP_port))
print("el Servidor está listo")
while True:
    message, clientAddress = serverSock.recvfrom(2048)
    print(message.decode())
    messageBack = input("Introduce mensaje: ")
    serverSock.sendto(messageBack.encode(), clientAddress)
    if messageBack == "FIN":
        break
serverSock.close()
