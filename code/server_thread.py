# server_thread.py
import socket
from threading import Thread


def server(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(address)
    s.listen(5)

    while True:
        client, addr = s.accept()
        print(f'Client connected from {addr}')
        Thread(target=connection_handler, args=(client, )).start()


def connection_handler(client):
    while True:
        data = client.recv(10000)
        if not data:
            break
        client.sendall(data)
    print('Connection closed')
    client.close()


if __name__ == '__main__':
    server(('localhost', 9999))
