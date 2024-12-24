import socket

serverAddress = "127.0.0.1"
serverPort = 19000
clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect((serverAddress, serverPort))
receivedMessage = clientSock.recv(1024)
print(receivedMessage.decode())
clientSock.close()
