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

def send_to_client(socket_client):
    socket_client.send("hi".encode())
    msg_recieved = socket_client.recv(1024)
    print("message recieved" + msg_recieved.decode())

def download(socket_client):
    file_names = ["cat.jpg,", "sunflower.jpg", "baloon.jpg"]
    string_arr_json = json.dumps(file_names)
    string_arr_json_len = len(string_arr_json)
    packed_length = string_arr_json_len.to_bytes(4)
    print(packed_length)

    socket_client.send(packed_length)
    socket_client.send(json.dumps(file_names).encode())
    print("sent array of names")
    raw = socket_client.recv(4)
    length = int.from_bytes(raw)
    print(length)
    message = ""
    result = ""
    while length > 0:
        message = socket_client.recv(1024).decode()
        length = length - 1024
        result = result + message
    print("we got a message that says " + result)
    #check that the file exists
    file_handle = open("files/" + result,"rb")
    file_content = file_handle.read()
    file_content_len = len(file_content)
    socket_client.send(file_content_len.to_bytes(4))
    socket_client.send(file_content)
    print("sent file content")



def upload(socket_client):

    raw = socket_client.recv(4)
    length = int.from_bytes(raw)
    print(length)
    message = ""
    file_name = ""
    while length > 0:
        message = socket_client.recv(1024).decode()
        length = length - 1024
        file_name = file_name + message

    print("file name is" + file_name)
    raw = socket_client.recv(4)
    length = int.from_bytes(raw)
    print(length)
    message = ""
    file_content = ""
    file_handle = open("files/" + file_name, "wb")
    while length > 0:
        message1 = socket_client.recv(1024)
        length = length - 1024
        file_handle.write(message1)

    print("file content is " + file_content)
    file_handle.close()

def main():

    socket_server, socket_client  = create_server()
    result = socket_client.recv(1024).decode()

    print("result is -=" + result + "=-")

    if result == "download":
        download(socket_client)
    elif result == "upload":
        upload(socket_client)
    else:
        socket_server.close()
        socket_client.close()

main()
