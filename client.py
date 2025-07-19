import socket

def download(s):
    s.send("download".encode())
    raw = s.recv(4)
    length = int.from_bytes(raw)
    print(length)
    result = ""
    message = ""
    while length > 0:
        message = s.recv(1024).decode()
        length = length - 1024
        result = result + message
    print("we got a message that says " + result)

    file_name = input("which file do you want to download?"
                      " if you send a nonexistent file name the process will stop")
    s.send((len(file_name)).to_bytes(4))
    print(len(file_name))
    s.send(file_name.encode())
    message1 = ""
    file_content = ""
    raw = s.recv(4)
    length = int.from_bytes(raw)
    print(length)

    file_handle = open(file_name, 'wb')

    while length > 0:
        message1 = s.recv(1024)
        length = length - 1024
        file_handle.write(message1)

    file_handle.close()


def upload(s):
    s.send("upload".encode())
    path = input("enter a file path you want to upload")

    file_name = path.split("/")[-1]
    s.send(len(file_name).to_bytes(4))
    s.send(file_name.encode())
    file_handle = open(path,"rb")

    file_content = file_handle.read()
    s.send(len(file_content).to_bytes(4))
    s.send(file_content)
    print("finished uploading")


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