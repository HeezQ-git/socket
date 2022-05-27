import socket
from _thread import *
from common import *
from time import sleep
import uuid

users = {
    'matt': 'admin',
    'wiktor': 'silnehaslo',
    'hubert': 'kasztany123'
}

auth_users = []

messages = []

def server_client(client, addr):
    data = ''
    while 'quit' not in data:
        data = get_data(client)
        rawdata = data
        data = data.replace("\end", "")
        args = data.split('\r\n')

        if args[0] == 'login':
            if args[1] in users and users[args[1]] == args[2]:
                sessionID = uuid.uuid4().hex
                auth_users.append(sessionID)
                send_response(client, 200, sessionID)
            else:
                send_response(client, 400, 'User doesn\'t exists')
        elif args[0] == 'send':
            sessionID = check_sessionID(rawdata)
            params = rawdata.split("\r\n")
            if sessionID == False or sessionID not in auth_users:
                send_response(client, 500, "Please log in")
            elif params[1] == params[2] == '' or params[1] not in users:
                send_response(client, 400, "User doesn't exist")
            else:
                messages.append((f'{params[4]}->{params[1]}', params[2]))
                send_response(client, 200, "Message sent successfully!")
        elif args[0] == 'list':
            sessionID = check_sessionID(rawdata)
            params = rawdata.split("\r\n")
            if sessionID == False or sessionID not in auth_users:
                send_response(client, 500, "Please log in")
            elif params[1] == params[2] == '' or params[2] not in users:
                send_response(client, 400, "User doesn't exist")
            else:
                final = []
                for x in messages:
                    if (f'{params[1]}' in x[0]) and (f'{params[2]}' in x[0]):
                        final.append(x)
                if len(final) > 0:
                    send_response(client, 200, str(final))
                else:
                    send_response(client, 600, "No messages were found")
        elif args[0] == 'clearchat':
            sessionID = check_sessionID(rawdata)
            params = rawdata.split("\r\n")
            if sessionID == False or sessionID not in auth_users:
                send_response(client, 500, "Please log in")
            elif params[1] == params[2] == '' or params[2] not in users:
                send_response(client, 400, "User doesn't exist")
            else:
                final = []
                c = 0
                for x in messages:
                    if (f'{params[1]}' in x[0]) and (f'{params[2]}' in x[0]):
                        del messages[messages.index(x)]
                        c += 1
                if c > 0:
                    send_response(client, 200, f"Successfully cleared chat between {params[2]} and {params[1]}.")
                else:
                    send_response(client, 600, "There are no messages between given users.")
        elif args[0] == 'userslist':
            send_response(client, 200, f'Users: ' + ', '.join(users.keys()))
        else:
            send_response(client, 300, "Command doesn't exist")
    s.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ip_connection)
    s.listen(5)

    try:
        while True:
            client, addr = s.accept()
            print("CONNECTED WITH ", addr[0])
            start_new_thread(server_client, (client, addr))
    except KeyboardInterrupt:
        s.close()
