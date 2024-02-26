import socket
import threading
import rsa

def init():
    public, private = rsa.newkeys(1024)

    return public, private 

def send_msg(client, public_partner, textqueue, sendqueue):
    while True:
        if len(sendqueue.queueData) > 0:
            message = sendqueue.pop()
            client.send(rsa.encrypt(message.encode(), public_partner))
            textqueue.push(f"You: {message}")

def recv_msg(client, private_key, textqueue):
    while True:
        textqueue.push("Other: " + rsa.decrypt(client.recv(1024), private_key).decode())

def mainscript(host, port, mode, textqueue, sendqueue):

    public, private = init()

    if mode == True:
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)

        serv.bind((host, port))
        textqueue.push(f"IP Address of server: {host}")
        textqueue.push(f"Port number of server: {port}")
        serv.listen()

        client, addr = serv.accept()

        client.send(public.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    
    elif mode == False:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        client.send(public.save_pkcs1("PEM"))

    send_thread = threading.Thread(target=send_msg, args=(client, public_partner, textqueue, sendqueue))
    recv_thread = threading.Thread(target=recv_msg, args=(client, private, textqueue))

    send_thread.start()
    recv_thread.start()



if __name__ == "__main__":
    mainscript()