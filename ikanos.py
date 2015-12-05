import threading
import socket
import time
import os

HOST = ''
PORT = 8888
BASE_DIR = 'www/'

def log(type, message):
    print(type + ": " + message)

class ClientThread(threading.Thread):
    def bytes_from_file(self, filename, chunksize=8192):
        result = []

        try:
            with open(filename, "rb") as f:
                while True:
                    chunk = f.read(chunksize)
                    if chunk:
                        result.append(chunk)
                    else:
                        break
        except:
            result = []

        return result

    def request_to_filename(self, request):
        request_string = request.decode('UTF-8')
        start = 5
        end = request_string.find("HTTP/1.") - 1

        return request_string[start:end]

    def get_filename(self, request_file_name):
        if not request_file_name:
            request_file_name = 'index.html'

        if not self.get_file_ext(request_file_name):
            request_file_name += '.html'

        return os.path.join(os.path.dirname(os.path.realpath(__file__)), BASE_DIR, request_file_name)

    def get_file_ext(self, file_name):
        extension = os.path.splitext(file_name)
        return extension[len(extension) - 1]

    def __init__(self, client_connection):
         self.client_connection = client_connection
         super(ClientThread, self).__init__()

    def get_header(self, response_code):
        result = "HTTP/1.0 " + str(response_code)

        if response_code == 200:
            result += " OK"
        else:
            result += " Not Found"

        result += "\n\n"
        return result

    def run(self):
        try:
            request = self.client_connection.recv(1024)

            file_name = self.request_to_filename(request)
            file_name = self.get_filename(file_name)

            log('Debug', "Request for: " + file_name)

            response = self.bytes_from_file(file_name)

            header = ""
            if response:
                header = self.get_header(200)
            else:
                header = self.get_header(404)
                response = self.bytes_from_file(self.get_filename("404.html"))

            log('Debug', "Response header: '" + header.strip() + "'")
        except:
            header = self.get_header(500)
            response = self.bytes_from_file(self.get_filename("500.html"))

        try:
            self.client_connection.sendall(bytes(header, 'UTF-8'))
            for i in response:
                self.client_connection.sendall(i)
        except:
            pass

        self.client_connection.close()
        log('Debug', 'Socket closed')


class Server:
    def serve(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((HOST, PORT))
        listen_socket.listen(1)
        print('Serving HTTP on port', PORT)

        while True:
            (clientsocket, address) = listen_socket.accept()
            log('Debug', 'New socket: ' + str(address))
            client = ClientThread(clientsocket)
            client.start()

if __name__ == "__main__":
    Server().serve()
