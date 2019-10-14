import socket
import queue
import selectors
import sys

from dojo.queue import SimpleQueue
from dojo.utils import socket_log, logger
from dojo.constants import (
    QUEUE_PATH,
    SERVER_ADDR,
    PACKET_SIZE,
    MAX_INCOMING,
    COMMANDS
)

class Server:
    def __init__(self, address, packet_size):
        self.selector = selectors.DefaultSelector()
        self.keep_running = True
        self.address = address
        self.packet_size = packet_size
        self.queue = SimpleQueue()
        
    def _read(self, connection, mask):
        """Callback that reads data from an existing socket connection
        
        It is binded to selectors hence executed anytime there's data
        to be read from a given `connection`"""
        try:
            client = connection.getpeername()
        except:
            logger.warning('{}:{} - ! Connection lost'.format(*connection.getsockname()))
            self.selector.unregister(connection)
            connection.close()
        else:
            data = connection.recv(self.packet_size)
            if data:
                # receieve
                socket_log(logger, client, 'recv')
                decoded_data = data.decode('utf-8')
                # process
                status, response = self._handle_request(decoded_data)
                # and send it back
                connection.sendall(response.encode('utf-8'))
                socket_log(logger, client, 'sent')
            else:
                socket_log(logger, client, 'close')
                # self.keep_running = False
                self.selector.unregister(connection)
                connection.close()
    
    def _accept(self, sock, mask):
        """Callback that accepts new socket connections
        
        It is binded to selectors hence executed anytime that a fresh
        connection is available. New connection is registered to selectors"""
        new_connection, addr = sock.accept()
        socket_log(logger, addr, 'new')
        new_connection.setblocking(False)
        self.selector.register(
            new_connection, selectors.EVENT_READ, self._read
        )
        
    def _build_command(self, object, action):
        """Creates queue-command string
        
        Obeys following template:
        {ACTION} {MODEL_NAME}"""
        return '{} {}'.format(action.upper(), object)
        
    def _process_command(self, decoded_data):
        """Processes a decoded server-command string
        
        Obeys following template:
        {OPERATION} {MODEL_NAME}
        """
        try:
            command, *rest = decoded_data.split(' ')
        except:
            raise
        if command not in COMMANDS:
            raise ValueError('Invalid command: {}'.format(command))
        
        queue_command = None
        if command == 'ENQUEUE':
            obj, action = rest
            queue_command = self._build_command(obj, action)
            self.queue.enqueue(queue_command)
        elif command == 'DEQUEUE':
            queue_command = self.queue.dequeue()
            if not queue_command:
                queue_command = ''

        return command, queue_command

    def _handle_request(self, decoded_data: str):
        """Parses a byte encoded request and returns accordingly"""
        try:
            command, response = self._process_command(decoded_data)
            status = 201 if command == 'ENQUEUE' else 200
            return (status, response)
        except ValueError as ex:
            return (400, str(ex))
        except Exception as ex:
            logger.warning(ex)
            return (500, str(ex))
    
    def run(self):
        """Runs the web server"""
        logger.info('Listening on {}'.format(self.address))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.bind(self.address)
        self.sock.listen(MAX_INCOMING)
        
        self.selector.register(
            self.sock, selectors.EVENT_READ, self._accept
        )
        
        while self.keep_running:
            for key, mask in self.selector.select():
                callback = key.data
                callback(key.fileobj, mask)
                
        logger.info('Closing doors')
        self.selector.close()
        
    def shutdown(self):
        if self.sock and self.selector:
            self.selector.close()
            self.sock.shutdown()
            self.sock.close()
    

if __name__ == '__main__':
    try:
        server = Server(SERVER_ADDR, PACKET_SIZE)
        server.run()
    except KeyboardInterrupt:
        server.shutdown()