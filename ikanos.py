import threading
import socket
import time
import os

class ClientThread(threading.Thread):
    base_dir = "./www/"

    def file_to_bytes(self, file_name):
        complete_file_name = os.path.dirname(os.path.realpath(__file__))
        complete_file_name = os.path.xjoin(complete_file_name, self.base_dir, file_name)

        myfile = open(complete_file_name, "r")
        data = ""
        lines = myfile.readlines()

        for line in lines:
            data = data + line.strip();

        data = bytes(data, 'UTF-8')
        return data

    def bytes_from_file(self, filename, chunksize=8192):
        result = []
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    result.append(chunk)
                else:
                    break
        return result

    def get_file_name(self, request):
        request_string = request.decode('UTF-8')

        start = 5
        end = request_string.find("HTTP/1.") - 1

        file_name = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(file_name, self.base_dir, request_string[start:end])

    def __init__(self, client_connection):
         self.client_connection = client_connection
         super(ClientThread, self).__init__()

    def run(self):
        request = self.client_connection.recv(1024)

        http_response = """\
HTTP/1.0 200 OK

"""
        data = self.bytes_from_file(self.get_file_name(request))

        self.client_connection.sendall(bytes(http_response, 'UTF-8'))

        for i in data:
            self.client_connection.sendall(i)

        self.client_connection.close()


class Server:
    def serve(self):
        HOST, PORT = '', 8888

        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((HOST, PORT))
        listen_socket.listen(1)
        print('Serving HTTP on port', PORT)

        while True:
            (clientsocket, address) = listen_socket.accept()
            client = ClientThread(clientsocket)
            client.start()

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
