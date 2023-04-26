# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import time

class Router:
    def __init__(self):
        self.routing_table = {}

    def print_table(self):
        print()
        print(f"| {'Destination':<20} | {'Output Interface':<20} | {'Metric':<10} |")
        print(f"| {'-'*20} | {'-'*20} | {'-'*10} |")
        for destination, values in self.routing_table.items():
            output_interface = values["output_interface"]
            metric = values["metric"]
            print(f"| {destination:<20} | {output_interface:<20} | {metric:<10} |")

    def update_routing_table(self, destination, output_interface, metric, connection):
        if destination not in self.routing_table:
            self.routing_table[destination] = {'output_interface': output_interface, 'metric': metric, 'connection': connection}
        elif metric < self.routing_table[destination]['metric']:
            self.routing_table[destination] = {'output_interface': output_interface, 'metric': metric, 'connection': connection}
        
    def send_package(self, source, destination, ttl, tos):
        if source not in self.routing_table:
            return f"Source IP address {source} not found in the routing table"
        else:
            output_interface = self.routing_table[destination]['output_interface']
            return f"Sending packet from {source} to {destination} via {output_interface}. TTL={ttl}, TOS={tos}"

    def handle_connection(self, conn, address):
        #print(f"Connection established by {address}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            type, data = data.decode().split(':')
            response = ""
            if type == "R":
                destination, output_interface, metric = data.split(',')
                self.update_routing_table(destination, output_interface, int(metric), conn)
                
            elif type == "M":
                source, destination, ttl, tos = data.split(',')
                response = self.send_package(source, destination, int(ttl), int(tos))
                value = self.routing_table.get(destination)
                if value is not None:
                    destination_connection = value['connection']
                    destination_connection.sendall(response.encode())
                else:
                    print("There is no value for", destination)
        conn.close()
        print(f"Connection closed by {address}")

