import socket
import json
import os

def create_server():

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(('127.0.0.1', 1800))
    socket_server.listen()
    print("server is listening")
    socket_client, client_address = socket_server.accept()
    print("got a client {}".format(client_address))
    return socket_server,socket_client

def send_to_client(socket_client, data, encode=True):

    data_len = len(data)
    packed_length = data_len.to_bytes(4)
    socket_client.send(packed_length)

    if encode:
        socket_client.send(data.encode())
    else:
        socket_client.send(data)

def accept_from_client(socket_client, file_handle):

    raw = socket_client.recv(4)
    length = int.from_bytes(raw)
    print(length)
    message = ""
    result = ""
    if file_handle:
        while length > 0:
            message1 = socket_client.recv(1024)
            length = length - 1024
            file_handle.write(message1)
    else:
        while length > 0:
            message = socket_client.recv(1024).decode()
            result = result + message
            length = length - 1024
    print("we got a message that says " + result)
    return result

def send_list(socket_client):
    dir_list = os.listdir("files")
    string_arr_json = json.dumps(dir_list)
    send_to_client(socket_client, string_arr_json, True)
    print("sent array of names")

def download(socket_client):

    file_name = accept_from_client(socket_client,None)
    if os.path.exists("files/" + file_name):
        file_handle = open("files/" + file_name,"rb")
        file_content = file_handle.read()
        send_to_client(socket_client, file_content, False)
        file_handle.close()
        print("sent file content")
    else:
        data_len = -1
        packed_length = data_len.to_bytes(4, signed=True)
        socket_client.send(packed_length)
        print("the file doesn't exist")



def upload(socket_client):

    file_name = accept_from_client(socket_client,None)
    print("file name is" + file_name)

    file_handle = open("files/" + file_name, "wb")
    file_content = accept_from_client(socket_client, file_handle)
    print("file content is " + file_content)

    file_handle.close()

def main():

    socket_server, socket_client  = create_server()
    while True:
        result = socket_client.recv(1024).decode()

        print("result is -=" + result + "=-")

        if result == "download":
            download(socket_client)
        elif result == "upload":
            upload(socket_client)
        elif result == "list":
            send_list(socket_client)
        else:
            break

    socket_server.close()
    socket_client.close()

main()
