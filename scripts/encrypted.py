import socket
import threading
import rsa

def init():
    public, private = rsa.newkeys(1024)

    public, private 

def send_msg(client, public_partner, textqueue, sendqueue):
    while True:

        if len(sendqueue.queueData) > 0:
            message = sendqueue.pop()
            client.send(rsa.encrypt(message.encode(), public_partner))
            print(f"You: {message}")
            textqueue.append(f"You: {message}")

def recv_msg(client, private_key, textqueue):
    while True:
        print("Other: " + rsa.decrypt(client.recv(1024), private_key).decode())
        textqueue.append("Other: " + rsa.decrypt(client.recv(1024), private_key).decode())

def mainscript(mode, textqueue):

    public, private = init()

    if mode == True:
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)

        port = int(input("Enter the port number you want to use: "))

        serv.bind((host, port))
        print(f"IP Address of server: {host}")
        print(f"Port number of server: {port}")
        serv.listen()

        client, addr = serv.accept()

        client.send(public.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    
    elif mode == False:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = input("Enter the IP of the host you want to connect to: ")
        port = int(input("Enter the port number that you want to use: "))
        client.connect((host, port))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        client.send(public.save_pkcs1("PEM"))

    send_thread = threading.Thread(target=send_msg, args=(client, public_partner, textqueue))
    recv_thread = threading.Thread(target=recv_msg, args=(client, private, textqueue))

    send_thread.start()
    recv_thread.start()



if __name__ == "__main__":
    mainscript()