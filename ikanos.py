import threading
import socket
import time

class ClientThread(threading.Thread):
    def __init__(self, client_connection):
         self.client_connection = client_connection
         super(ClientThread, self).__init__()

    def run(self):
        request = self.client_connection.recv(1024)
        print('------Started.')
        time.sleep(10)
        # print(request)

        http_response = """\
HTTP/1.0 200 OK

Hello, World!
"""

        self.client_connection.sendall(bytes(http_response, 'UTF-8'))
        self.client_connection.close()
        print('------Finished.')


class Server:
    def serve(self):
        HOST, PORT = '', 8888

        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((HOST, PORT))
        listen_socket.listen(1)
        print('Serving HTTP on port', PORT)

        while True:
            print('--Listening')
            (clientsocket, address) = listen_socket.accept()
            print('----Accepted')
            client = ClientThread(clientsocket)
            print('----Thread created')
            client.start()
            print('----Thread running')

# import socket
#
# while True:
#     client_connection, client_address = listen_socket.accept()
#     request = client_connection.recv(1024)
#     # print(request)
#
#     http_response = """\
# HTTP/1.0 200 OK
#
# Hello, World!
# """
#     client_connection.sendall(bytes(http_response, 'UTF-8'))
#     client_connection.close()

if __name__ == "__main__":
    Server().serve()
