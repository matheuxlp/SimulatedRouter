import socket
import time
import threading

class MockRouter:
    def __init__(self, id, destination_network, output_interface, metric):
        self.id = id
        # Set instance variables to the input parameters
        self.destination_network = destination_network
        self.output_interface = output_interface
        self.metric = metric
        # Set two other instance variables to specific values
        self.HOST = '127.0.0.1'
        self.PORT = 65432
        # Create a TCP/IP socket object
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to a server at the given host and port
        self.s.connect((self.HOST, self.PORT))


    def send(self):
        while True:
            data = f"R:{self.destination_network},{self.output_interface},{self.metric}".encode()
            self.s.sendall(data)
            time.sleep(30)

    def receive(self):
        while True:
            response = self.s.recv(1024)
            print(f"Mock Router #{self.id} receiving data: {response.decode()}")

    def __del__(self):
        self.s.close()


if __name__ == '__main__':
    # Create a list of MockRouter objects with different IP addresses, interface names, and metrics
    routers = [
        MockRouter(1 ,"192.168.0.1", "eth0", 1),
        MockRouter(2, "192.168.0.2", "eth1", 1),
        MockRouter(3, "192.168.0.3", "eth2", 1),
        MockRouter(4, "192.168.0.4", "eth3", 1)
    ]

    # Create a list of threads to call the send() method
    threads_send = []
    for router in routers:
        # Start a new thread to call the send() method of each MockRouter object
        thread_send = threading.Thread(target=router.send)
        thread_send.start()
        threads_send.append(thread_send)

    # Create a list of threads to call the receive() method
    threads_receive = []
    for router in routers:
        # Start a new thread to call the receive() method of each MockRouter object
        thread_receive = threading.Thread(target=router.receive)
        thread_receive.start()
        threads_receive.append(thread_receive)

    # Wait for all threads of send() to finish
    for thread_send in threads_send:
        thread_send.join()

    # Wait for all threads of receive() to finish
    for thread_receive in threads_receive:
        thread_receive.join()
