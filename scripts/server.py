import threading
import socket
import os

import psutil

import scripts.threadqueue as tq

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clients = []
nicknames = []

def broadcast(message: str):
    for client in clients:
        client.send(message)

def handle(client, textq: tq.ThreadQueue):
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
            textq.push(leftstr)
            broadcast(leftstr.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive(textq):
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
        textq.push(f"{nickname} has joined the chat!")
        broadcast(f"{nickname} has joined the chat!".encode('ascii'))

        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,textq))
        thread.start()
            


def main(port, textq, signalSend):
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)

    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            textq.push("This port is already in use!!")
            os._exit(0)

    print(f"IP address of host server is {host}")
    textq.push(f"IP address of host server is {host}")
    print(f"Server will be listening on port {port}")
    textq.push(f"Server will be listening on port {port}")

    server.bind((host, port))
    server.listen()
    print("Server is up and listening...")

    recvthread = threading.Thread(target=receive, args=(textq,))
    recvthread.start()

    while True:

        if signalSend.size > 0:
            recvthread.join()
            server.close()
            os._exit(0)