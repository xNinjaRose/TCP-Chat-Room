#! /usr/bin/python

import threading
import socket

#Connection information
host = "127.0.0.1"
port = 52005

#Start the server (SOCK_STREAM = TCP STREAM)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

#Lists for Clients and Their Nicknames
clients = []
nicknames = []

#Sending messages to all connected clients
def broadcast(message):
	for client in clients:
		client.send(message)

#Handling Messages from Clients
def handle(client):
	while True:
		try:
			#Broadcasting messages
			message = client.recv(1024)
			broadcast(message)
		except:
			#Removing and Closing Clients
			index = clients.index(client)
			clients.remove(client)
			clients.close()
			nickname = nicknames[index]
			broadcast(f"{nickname} left!".encode('ascii'))
			nicknames.remove(nickname)
			break

#Recieving/Listening Function
def receive():
	while True:
		#Accept Connection
		client,address = server.accept()
		print(f"Connected with{str(address)}")

		#Request and Store Nickname
		client.send('NICK'.encode('ascii'))
		nickname = client.recv(1024).decode('ascii')
		nicknames.append(nickname)
		clients.append(client)

		#Print and Broadcast Name
		print(f"Nickname is {nickname}")
		broadcast(f"{nickname} joined to the Chat!".encode("ascii"))
		client.send("Connected to Server!".encode("ascii"))

		#Start Handling Thread for Client
		thread = threading.Thread(target=handle, args=(client,))
		thread.start()

print("Server is listening...")

receive()
