import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import database
from password_manager import UserManager
from password_validator import PasswordValidator
from client import start_chat
from two_factor_auth import request_auth_code, verify_code  # Importa as funções de 2FA

# Criando uma instância do validador de senhas
password_validator = PasswordValidator()

# Criando a janela
jan = Tk()
jan.title("BatePapo")
jan.geometry("800x400")
jan.configure(background="white")
jan.resizable(width=False, height=False)
jan.attributes("-alpha", 0.95)
jan.iconbitmap(default="images/icon.ico")
logo = PhotoImage(file="images/logo.png")

# Frames
LeftFrame = Frame(jan, width=250, height=400, bg="#042c34", relief="raise")
LeftFrame.pack(side=LEFT)

RightFrame = Frame(jan, width=545, height=400, bg="#042c34", relief="raise")
RightFrame.pack(side=RIGHT)

# Logo
LogoLabel = Label(LeftFrame, image=logo, bg="#042c34")
LogoLabel.place(x=0, y=95)

# Labels e Entradas
UserLabel = Label(RightFrame, text="Usuário:", font=("Arial", 18), bg="#042c34", fg="#ffb370")
UserLabel.place(x=80, y=100)
UserEntry = ttk.Entry(RightFrame, width=43)
UserEntry.place(x=175, y=107)

PassLabel = Label(RightFrame, text="Senha:", font=("Arial", 18), bg="#042c34", fg="#ffb370")
PassLabel.place(x=80, y=140)
PassEntry = ttk.Entry(RightFrame, width=43, show="*")
PassEntry.place(x=175, y=147)

def LoginToApp():
    user = UserEntry.get()
    password = PassEntry.get()

    database.cursor.execute("SELECT Password, Email FROM Users WHERE User = ?", (user,))
    VerifyLogin = database.cursor.fetchone()

    if VerifyLogin and UserManager.check_password(VerifyLogin[0], password):
        email = VerifyLogin[1]
        request_auth_code(user, email)  # Chama a função para solicitar o código
        request_auth_code_window(user)  # Abre a janela para inserir o código
    else:
        messagebox.showerror(title="Erro", message="Acesso negado! Verifique o usuário e senha novamente.")

def request_auth_code_window(user):
    # Criar uma nova janela para inserir o código
    code_window = Toplevel(jan)
    code_window.title("Código de Autenticação")

    Label(code_window, text="Insira o código enviado para seu e-mail:", font=("Arial", 14)).pack(pady=10)
    code_entry = Entry(code_window)
    code_entry.pack(pady=10)

    def verify_code_window():
        entered_code = code_entry.get()
        if verify_code(user, entered_code):  # Chama a função de verificação
            messagebox.showinfo(title="Login info", message="Login efetuado!")
            code_window.destroy()
            jan.destroy()  # Fecha a janela de login
            start_chat(user)  # Inicia o chat com o usuário logado
        else:
            messagebox.showerror(title="Erro", message="Código inválido ou expirado.")

    verify_button = Button(code_window, text="Verificar Código", command=verify_code_window)
    verify_button.pack(pady=10)

# Botões
LoginButton = ttk.Button(RightFrame, text="Login", width=25, command=LoginToApp)
LoginButton.place(x=85, y=200)

def Register():
    LoginButton.place_forget()
    RegisterButton.place_forget()
    
    EmailLabel = Label(RightFrame, text="Email:", font=("Arial", 18), bg="#042c34", fg="#ffb370")
    EmailLabel.place(x=80, y=180)
    EmailEntry = ttk.Entry(RightFrame, width=43)
    EmailEntry.place(x=175, y=187)

    NameLabel = Label(RightFrame, text="Nome:", font=("Arial", 18), bg="#042c34", fg="#ffb370")
    NameLabel.place(x=80, y=220)
    NameEntry = ttk.Entry(RightFrame, width=43)
    NameEntry.place(x=175, y=227)

    def RegisterToDataBase():
        User = UserEntry.get()
        Password = PassEntry.get()
        Email = EmailEntry.get()
        Name = NameEntry.get()

        if not all([User, Password, Email, Name]):
            messagebox.showerror(title="Erro", message="Preencha todos os campos!")
            return

        if not password_validator.validate(Password):
            messagebox.showerror(title="Erro", message="A senha deve ter pelo menos 8 caracteres, uma letra maiúscula, um número e um caractere especial.")
            return
        
        print("Senha válida:", Password) if password_validator.validate(Password) else print("Senha inválida:", Password)

        try:
            hashed_password = UserManager.hash_password(Password)
            database.cursor.execute("""
            INSERT INTO Users(User, Password, Email, Name) VALUES(?, ?, ?, ?)
            """, (User, hashed_password, Email, Name))
            database.conn.commit()
            messagebox.showinfo(title="Situação", message="Cadastro efetuado!")
        except sqlite3.OperationalError as e:
            messagebox.showerror(title="Erro", message="Erro ao registrar: " + str(e))
        except Exception as e:
            messagebox.showerror(title="Erro", message="Erro inesperado: " + str(e))

    RegisterButton2 = ttk.Button(RightFrame, text="Registrar", width=43, command=RegisterToDataBase)
    RegisterButton2.place(x=130, y=270)

    def BackToLogin():
        EmailLabel.place_forget()
        EmailEntry.place_forget()
        RegisterButton2.place_forget()
        BackButton.place_forget()
        NameLabel.place_forget()
        NameEntry.place_forget()

        LoginButton.place(x=85, y=200)
        RegisterButton.place(x=280, y=200)
            
    BackButton = ttk.Button(RightFrame, text="Voltar", width=30, command=BackToLogin)
    BackButton.place(x=169, y=310)

RegisterButton = ttk.Button(RightFrame, text="Registrar", width=25, command=Register)
RegisterButton.place(x=280, y=200)

jan.mainloop()