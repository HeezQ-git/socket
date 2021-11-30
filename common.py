import socket
import math

ip_connection = ("localhost", 1768)

def get_data(socket_connection):
    data = b""
    while not b"\end" in data:
        data += socket_connection.recv(1)

    return data.decode("utf-8")

def send_data(socket_connection, data):
    socket_connection.sendall((data + "\end").encode("utf-8"))

def send_response(socket_connection, status_code, data):
    code_desc = ""
    
    if status_code == 200:
        code_desc = "OK"
    elif status_code == 300:
        code_desc = "Wrong command"
    elif status_code == 400:
        code_desc = "Wrong params for command"
    elif status_code == 500:
        code_desc = "Not authorised user"
    else:
        code_desc = "Unexpected error"
    
    socket_connection.sendall((str(status_code) + "\r\n" + code_desc + "\r\n" + data + "\end").encode("utf-8"))

def get_split_response(data):
    params = data.split("\r\n")
    return int(params[0]), params[1], params[2]

def check_sessionID(data):
    if "sessionID" in data:
        sessionID = data.split("sessionID:")[1].split("\r\n")[0]
        return sessionID
    return False

def fix_array(arr):
    if (arr == 'No messages were found'):
        return arr
    arr = arr.replace("[", "")
    arr = arr.replace("]", "")
    arr = arr.replace("(", "")
    arr = arr.replace(")", "")
    nArr = []
    tmp = arr.split("', ")
    for x in tmp:
        x = x.replace("'", "")
        nArr.append(x)
    final = []
    counter = 0
    while counter < len(nArr):
        final.append((nArr[counter].replace("->", " -> "), nArr[counter+1]))
        counter += 2
    return final