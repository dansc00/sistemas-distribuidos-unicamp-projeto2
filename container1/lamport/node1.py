import socket
import random
import json
import threading
import time

class ServerHandler:

    def __init__(self, HOST, PORT, DATA_PAYLOAD):

        self.HOST = HOST
        self.PORT = PORT
        self.DATA_PAYLOAD = DATA_PAYLOAD
    
    # abre servidor para receber conexão
    def openServerConnection(self, HOST, PORT, DATA_PAYLOAD):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket para conexão via IPv4 , utilizando TCP
        serverAddress = (HOST, PORT)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
        sock.bind(serverAddress) # vincula endereço de host e porta ao socket
        sock.listen(1) # socket entra em operação aguardando conexão de cliente, enfileirando uma conexão até que seja aceita
        print("Iniciando servidor no endereço {} porta {}...".format(HOST, PORT))
        i = 0
        while True:

            # aceita conexão, retorna uma tupla com um File Descriptor, usado para receber e enviar dados, e, o endereço do cliente
            conn, address = sock.accept()  
            data = conn.recv(DATA_PAYLOAD) # recebe dados do cliente
            if data:
                
                dataDecode = data.decode('utf-8') # decodifica dados em bytes para string
                dataJson = json.loads(dataDecode) # converte objeto string para JSON
                print("Mensagem recebida do  Processo{}".format(dataJson['senderID']))

                response = self.lamportClockAlgorithm(dataJson) # executa correção de relógio lógico
                responseStr = json.dumps(response) # converte em string
                conn.send(responseStr.encode('utf-8')) # envia resposta
                conn.close() # encerra conexão
            i += 1
            # realiza no máximo 10 conexões
            if i >= 10:
                break

class MessageHandler:

    def __init__(self, SERVER_HOST, PORT, DATA_PAYLOAD, message):

        self.SERVER_HOST = SERVER_HOST # ip do servidor
        self.PORT = PORT # porta para conexão
        self.DATA_PAYLOAD = DATA_PAYLOAD # tamanho máximo possível para transmissão de dados
        self.message = message # mensagem a ser enviada ao processo alvo

    # estabelece conexão com servidor no host e porta especificados e envia mensagem
    def sendMessage(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket IPv4, TCP/IP
        serverAddress = (self.SERVER_HOST, self.PORT) # define endereço com host e porta
        sock.connect(serverAddress) # conecta socket ao servidor
        try:

            messageStr = json.dumps(self.message) # serializa JSON em string
            sock.send(messageStr.encode('utf-8')) # envia mensagem codificada em bytes com UTF-8 
            #response = sock.recv(self.DATA_PAYLOAD) # mensagem de resposta recebida
            
        except socket.error as e:

            print("Socket error: {}".format(str(e)))
        except Exception as e:

            print("Other exception: {}".format(str(e)))
        finally:
            
            print("Closing connection")
            sock.close()

    # envia mensagem ao servidor proxy que irá repassar ao processo alvo
    def sendMessageToProcess(self, PROXY_HOST, TARGET_HOST, receiverID):
 
        # dicionario que irá transmitir objeto JSON, armazena id do processo remetente, id do processo destinatário, relógio lógico de Lamport
        message = {'senderID': self.ID, 'receiverID': receiverID, 'lamportClock': self.lamportClock, 'TARGET_HOST': TARGET_HOST} 
        newConnection = messageHandler.ClientMessageHandler(PROXY_HOST, 8000, 1024, message) 
        newConnection.sendMessage() # envia mensagem

class Process:

    def __init__(self, lamportClock, timeRate, numEvents, ID):

        self.lamportClock = lamportClock # armazena contador do relógio lógico de Lamport
        self.timeRate = timeRate # taxa de tempo que cada evento consome
        self.numEvents = numEvents # número de eventos realizados pelo processo
        self.ID = ID # id do processo

    def lamportClockAlgorithm(self, message):

        if(message['lamportClock'] >= self.getLamportClock()):

            self.setLamportClock(message['lamportClock'] + 1)
        else:

            self.setLamportClock(self.getLamportClock() + 1)

        response = {'lamportClock': self.getLamportClock()}

        return response
    

    # simula execução do processo, definindo uma taxa aleatória de tempo para os eventos e incrementando o relógio lógico a cada evento
    def simulatesProcessExecution(self):
        
        self.timeRate = random.randint(1,3) # define a taxa de variação do tempo como um valor entre 1 e 3
        self.numEvents = random.randint(1,5) # define o número de eventos ocorridos no processo como um valor entre 1 e 5

        # atribui valor ao relógio lógico de Lamport
        for i in range(self.numEvents):
            self.lamportClock = self.lamportClock + self.timeRate

    def getLamportClock(self):

        return self.lamportClock

    def setLamportClock(self, newLamportClock):

        self.lamportClock = newLamportClock


# executa apenas quando chamado diretamente, evita execução quando importado por outro script
if __name__ == "__main__":

    process1 = Process(0, 0, 0, 1) # inicializa Process1
    process1.simulatesProcessExecution() # simula execução de eventos

    HOSTNAME = socket.gethostname() # armazena hostname
    HOST = socket.gethostbyname(socket.gethostname()) # armazena host 

    openServerThread = threading.Thread(target=process1.openServerConnection, args=(HOST, 8000, 1024,))
    sendMessageThread2 = threading.Thread(target=process1.sendMessageToProcess, args=('172.18.0.5', '172.18.0.3', 2,))
    sendMessageThread3 = threading.Thread(target=process1.sendMessageToProcess, args=('172.18.0.5', '172.18.0.4', 3,))

    openServerThread.start()
    openServerThread.join()

    while True:
        sendMessageThread2.start()
        sendMessageThread2.join()
        time.sleep(2)

        sendMessageThread3.start()
        sendMessageThread3.join()
        time.sleep(2)

