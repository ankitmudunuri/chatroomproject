import socket
import threading


hostip = input("Type in the IP address of the server you want to connect to: ")
port = input("Type in the port that you would like to host this server on (default is 55555): ")
if (port == ""):
    port = 55555
else:
    port = int(port)
nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((hostip, port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(nickname.encode('ascii'))
            elif message == "INVALIDNICK":
                nicknamenew = input("That nickname is already taken or invalid, please use another nickname: ")
                client.send(nicknamenew.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred, and the connection has been closed")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()