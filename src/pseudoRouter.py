import socket
import time
import threading

def pseudoRouter(rede_destino, interface_saida, metrica):
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            data = f"R:{rede_destino},{interface_saida},{metrica}".encode()
            s.sendall(data)

            # Recebe a resposta do roteador simulado
            resposta = s.recv(1024)

            # Exibe a resposta na tela
            print(resposta.decode())

            time.sleep(1)

def main():
    threads = []
    threads.append(threading.Thread(target=pseudoRouter, args=('192.168.0.1', 'eth0', 2)))
    threads.append(threading.Thread(target=pseudoRouter, args=('10.0.0.1', 'wlan0', 3)))
    threads.append(threading.Thread(target=pseudoRouter, args=('172.16.0.1', 'eth1', 4)))
    threads.append(threading.Thread(target=pseudoRouter, args=('192.168.1.1', 'wlan1', 5)))


    for thread in threads:
        thread.start()

if __name__ == '__main__':
    main()
