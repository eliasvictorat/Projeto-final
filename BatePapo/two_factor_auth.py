import smtplib
import random
import string
from datetime import datetime, timedelta

# Dicionário para armazenar códigos e tempos de expiração
auth_codes = {}

def send_email(to_email, code):
    from_email = "andretestes79@gmail.com" 
    from_password = "zhvs yoxv dyhb jlyj" 

    subject = "Código de Autenticação"
    message = f"Seu código de autenticação é: {code}"

    email_message = f"Subject: {subject}\n\n{message}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            # Envia a mensagem
            server.sendmail(from_email, to_email, email_message.encode('utf-8'))
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar e-mail:", str(e))

def generate_auth_code():
    return ''.join(random.choices(string.digits, k=6))

def request_auth_code(user, email):
    # Gera código e armazena no dicionário
    code = generate_auth_code()
    auth_codes[user] = {'code': code, 'expiry': datetime.now() + timedelta(minutes=5)}

    # Envia código para o e-mail
    send_email(email, code)

def verify_code(user, entered_code):
    if user in auth_codes:
        auth_info = auth_codes[user]
        if entered_code == auth_info['code'] and datetime.now() < auth_info['expiry']:
            return True
    return False
