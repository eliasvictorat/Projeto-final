from socket import *
from threading import *

clients = set()

def clientThread(clientSocket, clientAddress):
    while True:
        encrypted_message = clientSocket.recv(1024)  # Recebe a mensagem criptografada
        print(f"Encrypted message from {clientAddress}: {encrypted_message}")

        # O servidor retransmite a mensagem criptografada para os outros clientes
        for client in clients:
            if client is not clientSocket:
                client.send(encrypted_message)

        if not encrypted_message:
            clients.remove(clientSocket)
            print(clientAddress[0] + ":" + str(clientAddress[1]) + " disconnected")
            break

    clientSocket.close()

hostSocket = socket(AF_INET, SOCK_STREAM)
hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

hostIp = "127.0.0.1"
portNumber = 7500
hostSocket.bind((hostIp, portNumber))
hostSocket.listen()
print("Waiting for connection...")

while True:
    clientSocket, clientAddress = hostSocket.accept()
    clients.add(clientSocket)
    print("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
    thread = Thread(target=clientThread, args=(clientSocket, clientAddress,))
    thread.start()