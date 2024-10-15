from cryptography.fernet import Fernet

# Gera uma chave e a salva
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Carrega a chave a partir do arquivo
def load_key():
    return open("secret.key", "rb").read()

# Função para criptografar uma mensagem
def encrypt_message(message):
    key = load_key()
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

# Função para descriptografar uma mensagem
def decrypt_message(encrypted_message):
    key = load_key()
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message
