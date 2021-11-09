import socket
from _thread import *
from common import *
from time import sleep

users = {
    'matt': 'admin',
    'wiktor': 'silnehaslo'
}

def server_client(client):
    data = get_data(client)
    data = data.replace("\end", "")

    sleep(3)

    args = data.split('\r\n')

    if args[0] == 'LOGIN':
        if users[args[1]] == args[2]:
            send_data(client, f'Zalogowano użytkownika o nazwie {args[1]}')
        send_data(client, f'Podano nieprawidłowe dane logowania!')
    else:
        send_data(client, 'Nie ma takiej komendy!')

    client.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ip_connection)
    s.listen(5)

    try:
        while True:
            client, addr = s.accept()
            print("CONNECTED WITH ", addr[0])
            start_new_thread(server_client, (client, ))
    except KeyboardInterrupt:
        s.close()