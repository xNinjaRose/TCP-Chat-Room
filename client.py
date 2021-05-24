#! /usr/bin/python

import socket
import threading

#Choosing the nickname
nickname = input("Choose your nickname: ")

#Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1",52005))

#Listening to Server and Sending nickname
def receive():
	while True:
		try:
			#Receive message from server
			#If "NICK" Send Nickname
			message = client.recv(1024).decode('ascii')
			if message == 'NICK':
				client.send(nickname.encode('ascii'))
			else:
				print(message)
		except:
			#close connection when error
			print("An error occured!")
			client.close()
			break

#Sending messages to the server
def write():
	while True:
		message = f"{nickname}: {input(' ')}"
		client.send(message.encode('ascii'))

#Starting threads for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
