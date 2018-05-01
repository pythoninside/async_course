# server.py
import socket
from loop9 import get_event_loop


def server(address, loop):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(False)
    s.bind(address)
    s.listen(5)

    while True:
        client, addr = yield from loop.sock_accept(s)
        print(f'Client connected from {addr}')
        loop.create_task(connection_handler(client, loop))


def connection_handler(client, loop):
    while True:
        data = yield from loop.sock_recv(client, 10000)
        if not data:
            break
        yield from loop.sock_sendall(client, data)
    print('Connection closed')
    client.close()


if __name__ == '__main__':
    loop = get_event_loop()
    task = loop.run_until_complete(server(('localhost', 9999), loop))
