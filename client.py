import socket
import threading
import tkinter as tk
from tkinter import simpledialog

# Configuração de conexão com o servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("192.168.15.7", 2424))

# Solicita o apelido do usuário
apelido = simpledialog.askstring("Apelido", "Digite seu apelido:")

def receber():
    while True:
        try:
            mensagem = cliente.recv(1024).decode("utf-8")
            if mensagem == f"{apelido} entrou no chat!":
                mensagem = "Você entrou no chat!"

            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, mensagem + "\n")
            chat_display.config(state=tk.DISABLED)
            chat_display.see(tk.END)
        except:
            print("Você foi desconectado do servidor!")
            cliente.close()
            break

def enviar_mensagem():
    mensagem = entrada_mensagem.get()
    cliente.send(mensagem.encode("utf-8"))
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Você: {mensagem}\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)
    entrada_mensagem.delete(0, tk.END)

def sair():
    cliente.close()
    window.quit()

cliente.send(apelido.encode("utf-8"))

window = tk.Tk()
window.title("Nosso chat Top")
window.geometry("250x300")  # Define um tamanho inicial maior para melhor visibilidade

header = tk.Frame(window, bg="purple", height=35)
header.pack(fill=tk.X)

title = tk.Label(header, text="Nosso chat TOP", bg="purple", fg="black", font=("times", 12, "bold"))
title.pack(side=tk.LEFT, padx=8, pady=4)

exit_button = tk.Button(header, text="SAIR", command=sair, bg="red", fg="white", font=("times", 12))
exit_button.pack(side=tk.RIGHT, padx=10, pady=5)

chat_frame = tk.Frame(window, bg="white")
chat_frame.pack(pady=(5, 0), padx=10, fill=tk.BOTH, expand=True)

chat_display = tk.Text(chat_frame, bg="white", font=("times", 12), wrap="word", state=tk.DISABLED)
chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

bottom_frame = tk.Frame(window)
bottom_frame.pack(fill=tk.X, padx=7, pady=7)

entrada_mensagem = tk.Entry(bottom_frame, font=("times", 10))
entrada_mensagem.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

send_button = tk.Button(bottom_frame, text="Enviar", command=enviar_mensagem, font=("times", 12), bg="purple", fg="white")
send_button.pack(side=tk.RIGHT)

receber_thread = threading.Thread(target=receber)
receber_thread.start()

window.mainloop()