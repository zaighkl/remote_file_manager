import os
import socket
import json

def get_file_names():
    socket_server = get_server_socket()
    socket_server.send("cmd_lst".encode())
    file_names_str = accept_from_server(False)
    file_names_arr = json.loads(file_names_str)
    return file_names_arr

_socket = None

def get_server_socket():
    global _socket

    if _socket is None:
        _socket = socket.socket()
        _socket.connect(('127.0.0.1', 1800))

    return _socket


def send_to_server(socket_server, data, encode=True):

    data_len = len(data)
    packed_length = data_len.to_bytes(4)
    socket_server.send(packed_length)

    if encode:
        socket_server.send(data.encode())
    else:
        socket_server.send(data)


def accept_from_server(file_handle):
    socket_server = get_server_socket()
    raw = socket_server.recv(4)
    length = int.from_bytes(raw, signed = True)
    print(length)

    if length == -1:
        raise Exception("the file doesn't exist :(((")

    result = ""
    if file_handle:
        while length > 0:
            message = socket_server.recv(1024)
            length = length - 1024
            file_handle.write(message)
    else:
        while length > 0:
            message = socket_server.recv(1024).decode()
            result = result + message
            length = length - 1024
    print("we got a message that says " + result)
    return result

def download(file_name):
    s = get_server_socket()
    s.send("cmd_dwn".encode())
    send_to_server(s,file_name,True)
    file_handle = open(file_name, 'wb')

    try:
        accept_from_server(file_handle)
        file_handle.close()
        return True
    except Exception as e:
        print(e)
        file_handle.close()
        os.remove(file_name)
        return False


def upload(path):
    s = get_server_socket()
    s.send("cmd_upl".encode())
    file_name = path.split("/")[-1]
    send_to_server(s, file_name, True)

    file_handle = open(path,"rb")
    file_content = file_handle.read()

    try:
        send_to_server(s,file_content, False)
        return True

    except:
        return False


if __file__ == 'main':
    main()