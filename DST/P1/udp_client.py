import socket

UDP_address = "127.0.0.1"
UDP_port = 16000
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    Message = input("Introduzca su mensaje en minúsculas: ")
    clientSock.sendto(Message.encode(), (UDP_address, UDP_port))
    modifiedMessage, address_received = clientSock.recvfrom(2048)
    print(modifiedMessage.decode())
    if modifiedMessage.decode() == "FIN":
        break
clientSock.close()
