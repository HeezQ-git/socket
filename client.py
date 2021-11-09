import socket
from common import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ip_connection)

print("CONNECTING, PLEASE WAIT...")
send_data(s, f"LOGIN\r\nmatt\r\nadmin")
data = get_data(s).replace("\end", "")
print(data)

s.close()
