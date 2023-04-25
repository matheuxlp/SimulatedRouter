import socket

def enviar_dado(origem, destino, ttl, tos):
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = f"M:{origem},{destino},{ttl},{tos}".encode()
        s.sendall(data)

        # Recebe a resposta do roteador simulado
        resposta = s.recv(1024)

        # Exibe a resposta na tela
        print(resposta.decode())

enviar_dado('192.168.0.1', '10.0.0.1', 10, 1)