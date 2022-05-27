import socket
from common import *

print('CONNECTING, PLEASE WAIT...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ip_connection)
print('CONNECTED!')

prefix = '@client'

user = input(prefix + ' - INPUT LOGIN => ')
password = input(prefix + ' - INPUT PASSWORD => ')
send_data(s, f'login\r\n{user}\r\n{password}')

data = get_data(s)

status_code, status_message, data = get_split_response(data)

if status_code == 200:
    sessionID = data.replace('\end', '') # ustawiamy sessionID po stronie klienta na wartość zwróconą ze strony serwera
    userLogged = user
    prefix = f'@{user}'
    print(f"Logged in!\nSSID: {sessionID}")
    while True:
        try:
            cmd = input(prefix + ' => ').lower()
            if cmd == 'exit' or cmd == 'quit':
                send_data(s, f"quit\r\n\r\n")
                break
            elif cmd == 'msg' or cmd == 'message' or cmd == 'send' or cmd.startswith('msg ') or cmd.startswith('message ') or cmd.startswith('send '):
                if ' ' in cmd:
                    params = cmd.split(' ')
                    person = params[1]
                    if len(params) > 2:
                        params.pop(0)
                        params.pop(0)
                        content = ' '.join(params)
                    else:
                        content = input(prefix + ' - input message content => ')
                else:
                    person = input(prefix + ' - to whom to send it? => ')
                    content = input(prefix + ' - input message content => ')
                send_data(s, f"send\r\n{person}\r\n{content}\r\nsessionID:{sessionID}\r\n{user}\r\n\r\n")
                data = get_data(s)
                
                status_code, status_message, data = get_split_response(data)
                print(f'{status_message}:', data.replace('\end', ''))
            elif cmd == 'list' or cmd == 'chat' or cmd.startswith('chat '):
                if ' ' in cmd:
                    person = cmd.split(' ')[1]
                else:
                    person = input(prefix + ' - whose chat do you want to see? => ')
                send_data(s, f"list\r\n{person}\r\n{user}\r\nsessionID:{sessionID}\r\n\r\n")
                data = get_data(s)
                
                status_code, status_message, data = get_split_response(data)
                if status_code == 200:
                    arr = fix_array(data.replace('\end', ''))
                    print(f' \nCHAT BETWEEN {user} AND {person}:\n')
                    for x in arr:
                        print(f'{x[0]}: {x[1]}')
                    print()
                else:
                    print(f'{status_message}:', data.replace('\end', ''))
            elif cmd == 'clearchat' or cmd == 'chatclear':
                person = input(prefix + ' - whose chat do you want to clear? => ')
                send_data(s, f"clearchat\r\n{person}\r\n{user}\r\nsessionID:{sessionID}\r\n\r\n")
                data = get_data(s)
                
                status_code, status_message, data = get_split_response(data)
                print(f'{status_message}:', data.replace('\end', ''))
            elif cmd == 'userslist':
                send_data(s, f"userslist\r\nsessionID:{sessionID}\r\n\r\n")
                data = get_data(s)
                
                status_code, status_message, data = get_split_response(data)
                print(f'{status_message}:', data.replace('\end', ''))
        except KeyboardInterrupt:
            print('CLOSING CONNECTION...')
            s.close()
            break
else:
    print(status_message, data.replace('\end', ''))

print('CLOSING CONNECTION...')
s.close()
