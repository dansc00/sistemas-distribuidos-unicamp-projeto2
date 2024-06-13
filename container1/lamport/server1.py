import socket

HOST = '172.17.0.3' # ip do host
PORT = 8000 # porta para conexão
DATA_PAYLOAD = 1024 # 

def server(HOST, PORT, DATA_PAYLOAD):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket para conexão via IPv4 , utilizando TCP
	print("Iniciando servidor no endereço %s porta %s" %(HOST, PORT))
	serverAddress = (HOST, PORT)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
	sock.bind(serverAddress) # vincula endereço de host e porta ao socket
	sock.listen(1) # socket entra em operação aguardando conexão de cliente, enfileirando uma conexão até que seja aceita
	i = 0
	while True:
		print("Esperando mensagem do cliente")
		conn, address = sock.accept() # aceita conexão, retorna uma tupla com endereço do cliente e um File Descriptor, usado para receber e enviar dados
		data = conn.recv(DATA_PAYLOAD) # recebe dados do cliente
		if data:
			print("Data: %s" %data)
			conn.send(data)
			print("Enviando %s para %s" % (data, address))
			conn.close() # end connection
		i += 1
		# realiza no máximo 3 conexões
		if i >= 3:
			break

server(HOST, PORT, DATA_PAYLOAD)