import os
import socket


def send_to_server(socket_server, data, encode=True):

    data_len = len(data)
    packed_length = data_len.to_bytes(4)
    socket_server.send(packed_length)

    if encode:
        socket_server.send(data.encode())
    else:
        socket_server.send(data)


def accept_from_server(socket_server, file_handle):

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

def download(s):
    s.send("download".encode())

    file_names_arr = accept_from_server(s,False)
    file_name = input("which file do you want to download")

    send_to_server(s,file_name,True)

    file_handle = open(file_name, 'wb')

    try:
        accept_from_server(s,file_handle)
        file_handle.close()
    except Exception as e:
        print(e)
        file_handle.close()
        os.remove(file_name)


def upload(s):
    s.send("upload".encode())
    path = input("enter a file path you want to upload")
    if os.path.exists(path):

        file_name = path.split("/")[-1]
        send_to_server(s,file_name,True)

        file_handle = open(path,"rb")
        file_content = file_handle.read()

        send_to_server(s,file_content,False)
        print("finished uploading")
    else:
        print("this file path doesn't exist on your computer")


def main():
    s = socket.socket()
    s.connect(('127.0.0.1', 1800))
    while True:
        status = input("do you want to upload or download file. press anything else to exit")
        if status == "download":
            download(s)
        elif status == "upload":
            upload(s)
        else:
            break

    s.close()
main()