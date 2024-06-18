import socket
import json

class LamportClockProxy:

	def __init__(self, HOST, PORT, DATA_PAYLOAD, processes):

		self.HOST = HOST # ip do host
		self.PORT = PORT # porta para conexão
		self.DATA_PAYLOAD = DATA_PAYLOAD # tamanho máximo possível para transmissão de dados
		self.processes = processes # vetor que armazena relógios lógicos de cada processo

	def printOutput(self):

		print("{}		{}		{}".format(self.processes[0], self.processes[1], self.processes[2]))

	# Encaminha mensagem recebida do processo remetente para o processo destinatário
	def forwardMessage(self, message):

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket IPv4, TCP/IP
		serverAddress = (message['receiverID'], self.PORT) # define endereço com host e porta
		sock.connect(serverAddress) # conecta socket ao servidor

		try:

			messageJson = json.dumps(message) # serializa JSON em string
			sock.send(messageJson.encode('utf-8')) # envia mensagem codificada em bytes com UTF-8 
			response = sock.recv(self.DATA_PAYLOAD) # mensagem de resposta recebida
		except socket.error as e:

			print("Socket error: {}".format(str(e)))
		except Exception as e:

			print("Other exception: {}".format(str(e)))
		finally:
			
			print("Closing connection")
			sock.close()
		
		return response

	# abre servidor para receber conexão
	def openConnection(self):

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket para conexão via IPv4 , utilizando TCP
		serverAddress = (self.HOST, self.PORT)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
		sock.bind(serverAddress) # vincula endereço de host e porta ao socket
		sock.listen(1) # socket entra em operação aguardando conexão de cliente, enfileirando uma conexão até que seja aceita
		print("Iniciando servidor proxy no endereço {} porta {}...".format(self.HOST, self.PORT))
		print("Relógios Lógicos")
		print("Processo1		Processo2		Processo3")
		while True:

            # aceita conexão, retorna uma tupla com um File Descriptor, usado para receber e enviar dados, e, endereço do cliente
			conn, address = sock.accept() 
			data = conn.recv(self.DATA_PAYLOAD) # recebe dados do cliente, no caso, o arquivo JSON da mensagem
			if data:
				
				dataDecode = data.decode('utf-8') # decodifica mensagem em bytes para string
				dataJson = json.loads(dataDecode) # converte em JSON

				# encaminha mensagem para o processo alvo e recebe o relógio lógico atualizado como resposta
				response = self.forwardMessage(dataJson) 
				responseDecode = response.decode('utf-8') # decodifica resposta
				responseJson = json.loads(responseDecode) # converte em JSON
				self.processes[dataJson['receiverID']-1] = responseJson['lamportClock'] # atualiza vetor de relógios lógicos 
				self.printOutput() # imprime saída
				
				responseStr = json.dumps(responseJson) # converte em string
				conn.send(responseStr.encode('utf-8')) # envia resposta
				conn.close() # encerra conexão
			
HOSTNAME = socket.gethostname() # armazena hostname
HOST = socket.gethostbyname(socket.gethostname()) # armazena host 
newConnection = LamportClockProxy(HOST, 8000, 1024, [0,0,0])
newConnection.openConnection() # abre para receber conexão

