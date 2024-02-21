import threading
import socket

import scripts.threadqueue as tq

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clients = []
nicknames = []

def broadcast(message: str):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            leftstr = f"{nickname} has left the chat"
            print(leftstr)
            broadcast(leftstr.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('ascii'))

        invalidflag = True

        nickname = ""
 
        nickname = client.recv(1024).decode('ascii')
        while invalidflag:
            if nickname in nicknames:
                client.send("INVALIDNICK".encode('ascii'))
                nickname = client.recv(1024).decode('ascii')
            else:
                break

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of connected client is {nickname}")
        broadcast(f"{nickname} has joined the chat!".encode('ascii'))

        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == "__main__":
    #hostname = socket.gethostname()
    #host = socket.gethostbyname(hostname)

    host = '127.0.0.1'

    port = input("Type in the port that you would like to host this server on (default is 55555): ")
    if (port == ""):
        port = 55555
    else:
        port = int(port)

    print(f"IP address of host server is {host}")
    print(f"Server will be listening on port {port}")

    server.bind((host, port))
    server.listen()
    print("Server is up and listening...")
    receive()