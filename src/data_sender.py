import socket

class DataSender:
    def __init__(self, origin, destination, ttl, tos):
        self.host = '127.0.0.1'
        self.port = 65432
        self.origin = origin
        self.destination = destination
        self.ttl = ttl
        self.tos = tos

    def send_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            data = f"M:{self.origin},{self.destination},{self.ttl},{self.tos}".encode()
            s.sendall(data)

            # Receives the response from the simulated router
            response = s.recv(1024)

            # Displays the response on the screen
            print(response.decode())

if __name__ == '__main__':
    sender = DataSender('192.168.0.1', '192.168.0.2', 5, 1)
    sender.send_data()