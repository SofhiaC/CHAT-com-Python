import threading
import socket

host = "192.168.15.7"
port = 2424

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clientes = {}
apelidos = {}


def broadcast(mensagem, sender=None):
    for apelidos, cliente in clientes.items():
        if cliente != sender:  # Não enviar de volta para o remetente
            cliente.send(mensagem.encode("utf-8"))


def tipo_mensagem(cliente, nickname):
    while True:
        try:
            mensagem = cliente.recv(1024).decode("utf-8")

            if mensagem.startswith("@"):
                # Unicast mensagem
                apelido_alvo = mensagem.split(" ")[0][1:]
                if apelido_alvo in clientes:
                    target_cliente = clientes[apelido_alvo]
                    target_cliente.send(f"{nickname} (privado): {' '.join(mensagem.split(' ')[1:])}".encode("utf-8"))
                else:
                    cliente.send(f"{apelido_alvo} não está conectado.".encode("utf-8"))
            else:
                # Broadcast mensagem para todos, exceto o remetente
                broadcast(f"{nickname}: {mensagem}", sender=cliente)
        except:
            # Remover clientee em caso de erro
            address = cliente.getpeername()  # Obter IP e porta do clientee
            cliente.close()
            del clientes[nickname]
            broadcast(f"{nickname} saiu do chat.")
            print(f"{nickname} (IP: {address[0]}, Porta: {address[1]}) saiu do chat")
            break


def entrada():
    while True:
        cliente, address = server.accept()
        cliente.send("NICK".encode("utf-8"))
        nickname = cliente.recv(1024).decode("utf-8")
        clientes[nickname] = cliente

        print(f"{nickname} entrou com IP: {address[0]}, Porta: {address[1]}")
        broadcast(f"{nickname} entrou no chat!")

        thread = threading.Thread(target=tipo_mensagem, args=(cliente, nickname))
        thread.start()


print("Servidor está funcionando e rodando...")
entrada()