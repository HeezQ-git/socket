import socket

ip_connection = ('localhost', 1768)

def get_data(socket_connection):
    data = b''
    while not b'\end' in data:
        data += socket_connection.recv(1)

    return data.decode('utf-8')

def send_data(socket_connection, data):
    socket_connection.sendall((data + '\end').encode('utf-8'))