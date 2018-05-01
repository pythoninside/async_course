# client.py
import socket
import time


def client(address, n):
    host, port = address

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    t0 = time.time()
    for i in range(n):
        s.send(b'Hello')
        s.recv(10000)
    dt = time.time() - t0
    print(f'{n / dt:.02f} roundtrip/s')


if __name__ == '__main__':
    client(('localhost', 9999), 500000)
