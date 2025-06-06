import socket

def connect_to_server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost', 8080))
	response = s.recv(1024)
	print(response)
	# Socket never closed

connect_to_server()