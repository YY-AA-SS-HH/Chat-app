import socket
import threading

import rsa
import tkinter as tk

public_key, private_key = rsa.newkeys(1024)
public_partner = None


choice = input("Do you want to host (1) or to connect (2) :")

if choice == "1":
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()),9999))
    server.listen()

    client , _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))



elif choice == "2":
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((socket.gethostbyname(socket.gethostname()),9999))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
else:
    exit()


def send(client):
    while True:
        msg = input("")
        client.send(rsa.encrypt(msg.encode(),public_partner))
        print("You: " + msg)





def recieve(client):
    while True:
        
        print("Friend: " + rsa.decrypt(client.recv(1024),private_key).decode())

        if client.recv(1024).decode() == "Q":
            client.close()
            break
        print("friend left chat room")




threading.Thread(target=send, args=(client,)).start()
threading.Thread(target=recieve, args=(client,)).start()
