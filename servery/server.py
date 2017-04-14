# -*- coding: utf-8 -*-

class Server(object):
    """Server is a web server class.
    
    :param host: host
    :param port: port
    :param handler: use to handle request
    """
    
    def __init__(self, host, port, handler):
        import socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.handler = handler
    
    def serve_forever(self):
        while True:
            client_socket, client_address = self.socket.accept()
            self.handle_request(client_socket, client_address)
            
    def handle_request(self, client_socket, client_address):
        self.handler(self, client_socket, client_address)