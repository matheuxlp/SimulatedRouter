import threading
import socket

from src import router as Router
from src import mock_router as Mock

class Main():
    def __init__(self):
        self.router = Router.Router()
    
    def run(self):
        HOST = '127.0.0.1'
        PORT = 65432

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()

            print("Starting Simulated Router...\n")

            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=self.router.handle_connection, args=(conn, addr))
                t.start()
            
if __name__ == '__main__':
    main = Main()
    main.run()