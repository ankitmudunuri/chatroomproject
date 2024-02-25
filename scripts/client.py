import socket
import threading

def receive(nickname, client, textq):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(nickname.encode('ascii'))
            else:
                textq.push(message)
        except:
            textq.push("An error occurred, and the connection has been closed")
            client.close()
            break

def write(nickname, client, sendq):
    while True:
        if sendq.size > 0:
            text = sendq.pop()
            message = f'{nickname}: {text}'
            client.send(message.encode('ascii'))

def main(hostip, port, nickname, textq, sendq):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((hostip, port))  

    receive_thread = threading.Thread(target=receive, args=(nickname, client, textq))
    receive_thread.start()
    write_thread = threading.Thread(target=write, args=(nickname, client, sendq))
    write_thread.start()