import threading

class ClientThread(threading.Thread):
     def __init__(self, client_connection):
         super(ClientThread, self).__init__()

     def run(self):
         print("BCT")


class Server:
    def serve(self):
        while True:

            # accept connections from outside
            (clientsocket, address) = serversocket.accept()
            # now do something with the clientsocket
            # in this case, we'll pretend this is a threaded server
            client = ClientThread(clientsocket)
            client.run()

import socket

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port', PORT)

while True:
    client_connection, client_address = listen_socket.accept()
    print('Accepted')
    request = client_connection.recv(1024)
    print(request)
    # print(request)

    http_response = """\
HTTP/1.0 200 OK

Hello, World!
"""
    client_connection.sendall(bytes(http_response, 'UTF-8'))
    client_connection.close()

# if __name__ == "__main__":
#     Server().serve()
