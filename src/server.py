import socket
import threading

class Roteador:
    def __init__(self):
        self.tabela_de_rotas = {}

    def atualizar_tabela_de_rotas(self, origem, destino, custo):
        if destino not in self.tabela_de_rotas:
            self.tabela_de_rotas[destino] = {'origem': origem, 'custo': custo}
        elif custo < self.tabela_de_rotas[destino]['custo']:
            self.tabela_de_rotas[destino] = {'origem': origem, 'custo': custo}

    def enviar_pacote(self, destino):
        if destino in self.tabela_de_rotas:
            print(f"Enviando pacote para {destino} via {self.tabela_de_rotas[destino]['origem']}")
        else:
            print(f"Não foi possível encontrar uma rota para {destino}")

def handle_client(conn, addr, roteador):
    print(f"Conectado por {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        origem, destino, custo = data.decode().split(',')
        roteador.atualizar_tabela_de_rotas(origem, destino, int(custo))
    conn.close()
    print(f"Conexão fechada por {addr}")

def server():
    roteador = Roteador()

    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr, roteador))
            t.start()

def main():
    server()

if __name__ == '__main__':
    main()
