import threading
import socket

# Tabela de roteamento do roteador simulado
tabela_roteamento = {
    'A': {'B': 2},
    'C': {'D': 3},
    'E': {'F': 4},
    'G': {'H': 5},
    'B': {'A': 2},
    'D': {'C': 3},
    'F': {'E': 4},
    'H': {'G': 5}
}

# Endereço IP e porta do roteador simulado
ROUTER_IP = '127.0.0.1'
ROUTER_PORT = 5000

def router():
    # Cria o socket do roteador simulado
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ROUTER_IP, ROUTER_PORT))
        s.listen()
        print(f'Roteador simulado iniciado em {ROUTER_IP}:{ROUTER_PORT}')
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f'Conexão estabelecida por {addr}')
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    mensagem, destino = data.decode().split(',')
                    print(f'Mensagem recebida: {mensagem}, destino: {destino}')
                    if destino in tabela_roteamento:
                        pseudo_router_ip, pseudo_router_port = tabela_roteamento[destino].popitem()
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pseudo_s:
                            pseudo_s.connect((pseudo_router_ip, pseudo_router_port))
                            pseudo_s.sendall(data)
                            resposta = pseudo_s.recv(1024).decode()
                            conn.sendall(resposta.encode())
                            print(f'Resposta do pseudo-roteador: {resposta}')

# Endereço IP e porta dos quatro pseudo-roteadores
PSEUDO_ROUTER_IPS = ['127.0.0.1', '127.0.0.1', '127.0.0.1', '127.0.0.1']
PSEUDO_ROUTER_PORTS = [6000, 6001, 6002, 6003]

def pseudoRouter(ip, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, porta))
        s.listen()
        print(f'Pseudo-roteador iniciado em {ip}:{porta}')
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f'Conexão estabelecida por {addr}')
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    mensagem, destino = data.decode().split(',')
                    print(f'Mensagem recebida: {mensagem}, destino: {destino}')
                    resposta = f'Mensagem recebida pelo pseudo-roteador {ip}:{porta}'
                    conn.sendall(resposta.encode())
                    print(f'Resposta do pseudo-roteador: {resposta}')

def main():
    # Inicia o roteador simulado em uma thread
    router_thread = threading.Thread(target=router)
   
