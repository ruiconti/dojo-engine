import selectors
import socket
import os
import multiprocessing

from dojo.constants import SERVER_ADDR, PACKET_SIZE
# from dojo.queue import SimpleQueue

class Client:
    def __init__(self, server_address=None):
        self.selector = selectors.DefaultSelector()
        self.server_addr = server_address if server_address else SERVER_ADDR
        self.data_to_read = True
        self._connect_to_server()
    
    def _connect_to_server(self):
        try:
            self.sock = socket.socket()
            self.sock.connect(self.server_addr)
        except socket.error:
            print('Failed to talk to server {}'.format(self.server_addr))
            raise
        else:
            self.sock.setblocking(False)
            self.selector.register(
                self.sock, selectors.EVENT_READ | selectors.EVENT_WRITE
            )
        # print('Successfully connected to {}'.format(self.server_addr))
        
    def _write(self, data):
        # print('[CLIENT] Sending {!r}'.format(data))
        self.sock.sendall(data)
        self.selector.modify(self.sock, selectors.EVENT_READ)
        
    def _read(self):
        data = self.sock.recv(PACKET_SIZE)
        if data:
            return data
        return False
        # self.data_to_read = False
        
    def send_data(self, data: bytes):
        received = False
        response_buff = []

        while not received:
            for key, mask in self.selector.select(timeout=1):
                if mask & selectors.EVENT_READ:
                    response = self._read()
                    if response:
                        response_buff.append(response)
                        received = True
                        
                if mask & selectors.EVENT_WRITE:
                    self._write(data)
                    
        return response_buff
        
    def shutdown(self):
        self.selector.unregister(self.sock)
        self.sock.close()
        self.selector.close()

