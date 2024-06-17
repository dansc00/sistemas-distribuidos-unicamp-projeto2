import socket
import json
import Process1 as process

class ServerConnectionHandler:

	def __init__(self, HOST, PORT, DATA_PAYLOAD):

		self.HOST = HOST # ip do host
		self.PORT = PORT # porta para conexão
		self.DATA_PAYLOAD = DATA_PAYLOAD # tamanho máximo possível para transmissão de dados

	@staticmethod
	def lamportClockAlgorithm(message):

		currentLamportClock = process.process1.getLamportClock()

		if(message['lamportClock'] >= currentLamportClock):

			process.process1.setLamportClock(message['lamportClock'] + 1)
		else:

			process.process1.setLamportClock(currentLamportClock + 1)
		
		response = {'lamportClock': process.process1.getLamportClock()}

		return response
	
	def openConnection(self):

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket para conexão via IPv4 , utilizando TCP
		serverAddress = (self.HOST, self.PORT)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
		sock.bind(serverAddress) # vincula endereço de host e porta ao socket
		sock.listen(1) # socket entra em operação aguardando conexão de cliente, enfileirando uma conexão até que seja aceita
		print("Iniciando servidor no endereço {} porta {}...".format(self.HOST, self.PORT))
		i = 0
		while True:

			# aceita conexão, retorna uma tupla com um File Descriptor, usado para receber e enviar dados, e, o endereço do cliente
			conn, address = sock.accept()  
			data = conn.recv(self.DATA_PAYLOAD) # recebe dados do cliente
			if data:
				
				dataDecode = data.decode('utf-8') # decodifica dados em bytes para string
				dataJson = json.loads(dataDecode) # converte objeto string para dicionário
				print("Mensagem recebida do  Processo{}".format(dataJson['senderID']))

				response = self.lamportClockAlgorithm(dataJson)
				responseStr = json.dumps(response)
				conn.send(responseStr.encode('utf-8'))
				conn.close() # encerra conexão
			i += 1
			# realiza no máximo 10 conexões
			if i >= 10:
				break

HOSTNAME = socket.gethostname() # armazena hostname
HOST = socket.gethostbyname(socket.gethostname()) # armazena host 
newConnection = ServerConnectionHandler(HOST, 8000, 1024) 
newConnection.openConnection() # abre para receber conexão