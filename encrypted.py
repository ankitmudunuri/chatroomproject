import socket
import threading
import rsa

def init():
    mode = input("Host mode (h) or client mode (c): ")
    mode = mode.lower()

    while True:
        if (mode != 'h') and (mode != 'c'):
            mode = input("Invalid input, input either 'h' for host mode or 'c' for client mode")
            mode = mode.lower()
        else:
            break

    public, private = rsa.newkeys(1024)

    return mode, public, private 

def send_msg(client, public_partner):
    while True:
        message = input("")

        client.send(rsa.encrypt(message.encode(), public_partner))
        print(f"You: {message}")

def recv_msg(client, private_key):
    while True:
        print("Other: " + rsa.decrypt(client.recv(1024), private_key).decode())

def main():

    mode, public, private = init()

    if mode == 'h':
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #hostname = socket.gethostname()
        #host = socket.gethostbyname(hostname)
        host = "127.0.0.1"

        port = int(input("Enter the port number you want to use: "))

        serv.bind((host, port))
        print(f"IP Address of server: {host}")
        print(f"Port number of server: {port}")
        serv.listen()

        client, addr = serv.accept()

        client.send(public.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    
    elif mode == 'c':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = input("Enter the IP of the host you want to connect to: ")
        port = int(input("Enter the port number that you want to use: "))
        client.connect((host, port))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        client.send(public.save_pkcs1("PEM"))

    send_thread = threading.Thread(target=send_msg, args=(client, public_partner))
    recv_thread = threading.Thread(target=recv_msg, args=(client, private))

    send_thread.start()
    recv_thread.start()



if __name__ == "__main__":
    main()