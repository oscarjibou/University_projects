import socket

serverAddress = "127.0.0.1"
serverPort = 19000
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind((serverAddress, serverPort))
print("el Servidor está listo")
serverSock.listen(5)
while True:
    clientSock, addr = serverSock.accept()
    print(f"Conexión desde {addr} establecida!")
    clientSock.send(bytes("Bienvenido al Servidor", "utf-8"))
    clientSock.close()
