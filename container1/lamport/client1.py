import socket

HOST = '172.17.0.2'
PORT = 8000
DATA_PAYLOAD = 1024	

def client(HOST, PORT, 	DATA_PAYLOAD):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket IPv4, TCP/IP
	print("Conectando ao endereço %s porta %s" %(HOST, PORT))
	serverAddress = (HOST, PORT)
	sock.connect(serverAddress) # conecta socket ao servidor
	try:
		message = "Teste"
		print("Enviando %s" %message)
		sock.send(message.encode('utf-8')) # envia dados codificados em string
		data = sock.recv(DATA_PAYLOAD)
		print("Recebido: %s" %data)
	except socket.error as e:
		print("Socket error: %s" %str(e))
	except Exception as e:
		print("Other exception: %s" %str(e))
	finally:
		print("Closing connection")
		sock.close()

client(HOST, PORT, DATA_PAYLOAD)