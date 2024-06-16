import socket
import random
import json

class ClientMessageHandler:

    def __init__(self, SERVER_HOST, PORT, DATA_PAYLOAD, MESSAGE):

        self.SERVER_HOST = SERVER_HOST # ip do servidor
        self.PORT = PORT # porta para conexão
        self.DATA_PAYLOAD = DATA_PAYLOAD # tamanho máximo possível para transmissão de dados
        self.MESSAGE = MESSAGE # mensagem a ser enviada ao servidor	

    # estabelece conexão com servidor no host e porta especificados
    def startConnection(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket IPv4, TCP/IP
        serverAddress = (self.SERVER_HOST, self.PORT) # define endereço com host e porta
        sock.connect(serverAddress) # conecta socket ao servidor
        try:
            MESSAGE_JSON = json.dumps(self.MESSAGE) # serializa JSON em string
            sock.send(MESSAGE_JSON.encode('utf-8')) # envia mensagem codificada em bytes com UTF-8 
            data = sock.recv(self.DATA_PAYLOAD) # mensagem de resposta recebida
        except socket.error as e:
            print("Socket error: {}".format(str(e)))
        except Exception as e:
            print("Other exception: {}".format(str(e)))
        finally:
            print("Closing connection")
            sock.close()

class Process:

    def __init__(self, lamportClock, timeRate, numEvents, id):

        self.lamportClock = lamportClock # armazena contador do relógio lógico de Lamport
        self.timeRate = timeRate # taxa de tempo que cada evento consome
        self.numEvents = numEvents # número de eventos realizados pelo processo
        self.id = id # id do processo

    # simula execução do processo, definindo uma taxa aleatório de tempo para os eventos e incrementando o relógio lógico a cada evento
    def simulatesProcessExecution(self):
        
        self.timeRate = random.randint(1,5) # define a taxa de variação do tempo como um valor entre 1 e 5
        self.numEvents = random.randint(1,10) # define o número de eventos ocorridos no processo como um valor entre 1 e 10

        for i in range(self.numEvents):
            self.lamportClock = self.lamportClock + self.timeRate

    def sendMessageForProcess1(self):
        SERVER_HOST = '172.18.0.5' # host do servidor
        TARGET_HOST = '172.18.0.2' # host do processo alvo
        # dicionario que irá transmitir objeto JSON, armazena id do processo remetente, id do processo destinatário, relógio lógico de Lamport
        MESSAGE = {'senderID': self.id, 'receiverID': 1, 'lamportClock': self.lamportClock, 'TARGET_HOST': TARGET_HOST} 
        newConnection = ClientMessageHandler(SERVER_HOST, 8000, 1024, MESSAGE)
        newConnection.startConnection()

    #def sendMessageForProcess3();

process2 = Process(0, 0, 0, 2)
process2.simulatesProcessExecution()
process2.sendMessageForProcess1()

