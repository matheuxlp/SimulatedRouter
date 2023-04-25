import socket
import time
import threading

def client(origem, destino, custo):
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            data = f"{origem},{destino},{custo}".encode()
            s.sendall(data)
            time.sleep(1)

def main():
    threads = []
    threads.append(threading.Thread(target=client, args=('A', 'B', 2)))
    threads.append(threading.Thread(target=client, args=('C', 'D', 3)))
    threads.append(threading.Thread(target=client, args=('E', 'F', 4)))
    threads.append(threading.Thread(target=client, args=('G', 'H', 5)))

    for thread in threads:
        thread.start()

if __name__ == '__main__':
    main()
