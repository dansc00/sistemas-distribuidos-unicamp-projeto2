import socket
import json

class LamportClock:

	def __init__(self, HOST, PORT, DATA_PAYLOAD):

		self.HOST = HOST # ip do host
		self.PORT = PORT # porta para conexão
		self.DATA_PAYLOAD = DATA_PAYLOAD # tamanho máximo possível para transmissão de dados

	# abre servidor para receber conexão
	def openConnection(self):

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket para conexão via IPv4 , utilizando TCP
		serverAddress = (self.HOST, self.PORT)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
		sock.bind(serverAddress) # vincula endereço de host e porta ao socket
		sock.listen(1) # socket entra em operação aguardando conexão de cliente, enfileirando uma conexão até que seja aceita
		print("Iniciando servidor no endereço {} porta {}...".format(self.HOST, self.PORT))
		print("Esperando mensagens dos clientes...")
		i = 0
		while True:
            # aceita conexão, retorna uma tupla com um File Descriptor, usado para receber e enviar dados, e, endereço do cliente
			conn, address = sock.accept() 
			data = conn.recv(self.DATA_PAYLOAD) # recebe dados do cliente, no caso, o arquivo JSON da mensagem
			if data:
				with open(data, 'rb') as dataFile:

					dataFile = data.read() 

				data
				dataJson = json.load(dataDecode) # converte mensagem de volta a dicionario
				print("Encaminhando mensagem do Processo{} para o Processo{}".format(dataJson['senderID'], dataJson['receiverID']))
				print("Data: {}".format(dataJson))
				data = json.dumps(dataJson)
				conn.send(data.encode('utf-8'))
				print("Enviando {}".format(data))
				conn.close() # end connection
			i += 1
			# realiza no máximo 3 conexões
			if i >= 3:
				break

HOSTNAME = socket.gethostname() # armazena hostname
HOST = socket.gethostbyname(socket.gethostname()) # armazena host 
newConnection = LamportClock(HOST, 8000, 1024)
newConnection.openConnection()

