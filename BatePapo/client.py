from socket import *
from threading import *
from tkinter import *
from encryption import encrypt_message, decrypt_message

def start_chat(username):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    hostIp = "127.0.0.1"
    portNumber = 7500

    clientSocket.connect((hostIp, portNumber))

    # Configuração da janela
    window = Tk()
    window.title("Conectado a: " + hostIp + ":" + str(portNumber))

    txtMessages = Text(window, width=50, state='disabled')  # Inicialmente desabilitado
    txtMessages.grid(row=0, column=0, padx=10, pady=10)

    txtYourMessage = Entry(window, width=50)
    txtYourMessage.insert(0, "Sua mensagem")
    txtYourMessage.grid(row=1, column=0, padx=10, pady=10)

    # Função para enviar mensagem
    def sendMessage():
        clientMessage = txtYourMessage.get()
        txtYourMessage.delete(0, END) 
        # Criptografa a mensagem antes de enviar
        encrypted_message = encrypt_message(username + ": " + clientMessage)

        txtMessages.config(state='normal')
        txtMessages.insert(END, "\n" + username + ": " + clientMessage)
        txtMessages.config(state='disabled') 

        clientSocket.send(encrypted_message)  # Envia a mensagem criptografada

    btnSendMessage = Button(window, text="Enviar", width=20, command=sendMessage)
    btnSendMessage.grid(row=2, column=0, padx=10, pady=10)

    # Função para receber mensagens
    def recvMessage():
        while True:
            encrypted_message = clientSocket.recv(1024)  # Recebe a mensagem criptografada
            try:
                # Descriptografa a mensagem recebida
                decrypted_message = decrypt_message(encrypted_message)
                txtMessages.config(state='normal')
                txtMessages.insert(END, "\n" + decrypted_message)  # Mostra a mensagem descriptografada
                txtMessages.config(state='disabled')
            except Exception as e:
                # Caso ocorra um erro na descriptografia
                print(f"Erro ao descriptografar a mensagem: {e}")
                txtMessages.config(state='normal')
                txtMessages.insert(END, "\n[Mensagem criptografada recebida]")  # Se a descriptografia falhar
                txtMessages.config(state='disabled')

    # Inicia a thread para receber mensagens
    recvThread = Thread(target=recvMessage)
    recvThread.daemon = True
    recvThread.start()

    window.mainloop()

