import socket

class IpPacketSender:
    def __init__(self, ttl, tos):
        print("Creating data packet...\n")
        self.host = '127.0.0.1'  
        self.port = 65432  
        self.source = "" 
        self.destination = ""
        self.message = ""
        self.ttl = ttl  
        self.tos = tos  

    def get_data(self):
        while True:
            input_data = input("Enter data (source, destination, message) separated by commas: ")
            input_list = input_data.split(',')

            if len(input_list) != 3:
                print("Invalid input. Please enter data in the format 'source,destination,message'")
                continue
            else:
                user_source, user_destination, user_message = input_list
                if user_source == user_destination:
                    print("Source and destination must be different.")
                    continue
                else:
                    self.source = user_source
                    self.destination = user_destination
                    self.message = user_message
                    break
        print("{:<15} {:<15} {:<10} {:<10} {:<10}".format("Source", "Destination", "TTL", "TOS", "Message"))
        print("{:<15} {:<15} {:<10} {:<10} {:<10}".format(self.source, self.destination, self.ttl, self.tos, self.message))

    def send_data(self):
        print("Sending Packet...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
            s.connect((self.host, self.port))  
            data = f"M;{self.source},{self.destination},{self.ttl},{self.tos},{self.message}".encode()  
            s.sendall(data) 

    def run(self):
        self.get_data()
        self.send_data() 

if __name__ == '__main__':
    sender = IpPacketSender(5, 1) 
    sender.run()
