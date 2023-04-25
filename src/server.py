import socket
import threading

class Roteador:
    def __init__(self):
        self.tabela_de_rotas = {}

    def atualizar_tabela_de_rotas(self, destino, interface_saida, metrica, conn):
        if destino not in self.tabela_de_rotas:
            self.tabela_de_rotas[destino] = {'interface_saida': interface_saida, 'metrica': metrica, 'socket': conn}
        elif metrica < self.tabela_de_rotas[destino]['metrica']:
            self.tabela_de_rotas[destino] = {'interface_saida': interface_saida, 'metrica': metrica, 'socket': conn}
        #print(self.tabela_de_rotas)

    def enviar_pacote(self, destino):
        if destino in self.tabela_de_rotas:
            # Encaminha o pacote para o próximo roteador na rota
            proximo_roteador = self.tabela_de_rotas[destino]['interface_saida']
            print(f"Encaminhando pacote para {destino} via {proximo_roteador}")
            return 'Pacote encaminhado com sucesso'
        else:
            return f"Não foi possível encontrar uma rota para {destino}"
        
    def encaminhar_pacote(self, origem, destino, ttl, tos):
        print("here")
        if origem not in self.tabela_de_rotas:
            return f"Endereço IP de origem {origem} não encontrado na tabela de rotas"
        else:
            interface_saida = self.tabela_de_rotas[destino]['interface_saida']
            return f"Enviando pacote de {origem} para {destino} via {interface_saida}. TTL={ttl}, TOS={tos}"

def handle_client(conn, addr, roteador):
    print(f"Conectado por {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        type, data = data.decode().split(':')
        resposta = ""
        if type == "R":
            rede_destino, interface_saida, metrica = data.split(',')
            roteador.atualizar_tabela_de_rotas(rede_destino, interface_saida, int(metrica), conn)
            #resposta = roteador.enviar_pacote(rede_destino)
        elif type == "M":
            origem, destino, ttl, tos = data.split(',')
            resposta = roteador.encaminhar_pacote(origem, destino, int(ttl), int(tos))
            valor = roteador.tabela_de_rotas.get(destino)
            if valor is not None:
                socket_destino = valor['socket']
                socket_destino.sendall(resposta.encode())
            else:
                print("Não existe um valor para", destino)
        #print(conn)
        #conn.sendall(resposta.encode())
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
