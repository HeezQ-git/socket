# client -----------------------> server
#    LOGIN \r\n matt \r\n HASŁO \end
# 1) serwer sprawdza poprawność komendy (LOGIN) -> \r\n -> login -> \r\n -> hasło -> \end
# 2) serwer sprawdza czy w słowniku znajduje się user z takim hasłem
# 3) Jeżeli 2: -> tak => odpowiada, -> nie => odpowiada ... <- 200.OK.\end, <- 404. BAD LOGIN.\end

import socket
from common import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ip_connection)

print("CONNECTING, PLEASE WAIT...")
send_data(s, f"LOGIN\r\nmatt\r\nadmin")
data = get_data(s).replace("\end", "")
print(data)

s.close()