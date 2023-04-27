# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import time
import os

class Router:
    def __init__(self):
        # initialize the router with 0 received packages and an empty routing table
        self.received_packages = 0
        self.routing_table = {}
        print(f"Initilizing Simulated Router...\n")

    def print_table(self):
        # clear the console and print the routing table in a formatted table
        os.system('clear')
        print()
        print(f"| {'-'*5} | {'-'*20} | {'-'*20} | {'-'*10} |")
        print(f"| {'Id':<5} | {'Destination':<20} | {'Output Interface':<20} | {'Metric':<10} |")
        print(f"| {'-'*5} | {'-'*20} | {'-'*20} | {'-'*10} |")
        for destination, values in self.routing_table.items():
            output_interface = values["output_interface"]
            metric = values["metric"]
            id = values["id"]
            print(f"| {id:<5} | {destination:<20} | {output_interface:<20} | {metric:<10} |")
        print(f"| {'-'*5} | {'-'*20} | {'-'*20} | {'-'*10} |")

    def update_routing_table(self, destination, output_interface, metric, connection, id):
        # update the routing table with new information about a destination
        if destination not in self.routing_table:
            print(f"Connected to Mock Router #{id}")
            self.routing_table[destination] = {'output_interface': output_interface, 'metric': metric, 'connection': connection, 'id': id}
        elif metric < self.routing_table[destination]['metric']:
            self.routing_table[destination] = {'output_interface': output_interface, 'metric': metric, 'connection': connection, 'id': id}
        
    def send_package(self, source, destination, ttl, tos, message):
        # send a packet from a source to a destination using the routing table to determine the output interface
        if source not in self.routing_table:
            print(f"Source IP address {source} not found in the routing table")
        elif destination not in self.routing_table:
            print(f"Destination IP address {destination} not found in the routing table")
        else:
            destination_connection = self.routing_table[destination]['connection']
            data = f"{source},{destination},{ttl},{tos},{message}"
            destination_connection.sendall(data.encode())
        
    def handle_routing_packet(self, data, connection):
        # handle a routing packet received from a connected router
        destination, output_interface, metric, id = data.split(',')
        self.update_routing_table(destination, output_interface, int(metric), connection, id)

    def handle_ip_packet(self, data):
        # handle an IP packet received from a connected host
        source, destination, ttl, tos, message = data.split(',')
        ttl = str(int(ttl) - 1)
        if int(ttl) <= 0:
            print("TTL exceeded")
        else:
            self.send_package(source, destination, ttl, tos, message)

    def handle_connection(self, conn, address):
        # handle a new connection by receiving data and routing packets or updating the routing table
        while True:
            data = conn.recv(1024)
            if not data:
                break
            type, data = data.decode().split(':')
            if type == "R":
                self.handle_routing_packet(data, conn)
                self.received_packages += 1
                if self.received_packages == 4:
                    time.sleep(1)
                    self.print_table()
                    self.received_packages = 0
            elif type == "M":
                self.handle_ip_packet(data)
                #conn.close()
        conn.close()

