import socket
import random
import json
import threading
import time

class Process:

    def __init__(self, lamportClock, timeRate, numEvents, serverFlag, ID, HOST, PORT, DATA_PAYLOAD):

        self.lamportClock = lamportClock # armazena contador do relógio lógico de Lamport
        self.timeRate = timeRate # taxa de tempo que cada evento consome
        self.numEvents = numEvents # número de eventos realizados pelo processo
        self.ID = ID # id do processo
        self.HOST = HOST # endereço ip do host
        self.PORT = PORT # porta para gerenciar conexões
        self.DATA_PAYLOAD = DATA_PAYLOAD # tamanho máximo permitido para troca de dados
        self.serverFlag = serverFlag # flag marca se o servidor está em execução

    # corrige o relógio lógico do processo baseado na mensagem recebida
    def lamportClockAlgorithm(self, message):

        # verifica se o relógio lógico do remetente é maior que do destinatário
        if(message['lamportClock'] >= self.getLamportClock()):

            self.setLamportClock(message['lamportClock'] + 1) # atualiza relógio lógico do processo
        else:

            self.setLamportClock(self.getLamportClock() + 1)

    # simula execução do processo, definindo uma taxa aleatória de tempo para os eventos e incrementando o relógio lógico a cada evento
    def simulatesProcessExecution(self):
        
        self.timeRate = random.randint(1,3) # define a taxa de variação do tempo como um valor entre 1 e 3
        self.numEvents = random.randint(1,5) # define o número de eventos ocorridos no processo como um valor entre 1 e 5   
        self.lamportClock = self.timeRate + self.numEvents # atribui valor inicial ao relógio lógico de Lamport
 
    def getLamportClock(self):

        return self.lamportClock

    def setLamportClock(self, newLamportClock):

        self.lamportClock = newLamportClock
    
    # inicia conexões do servidor
    def openServerConnection(self, TARGET_ID, TARGET_HOST):

        if(self.serverFlag == False):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket para conexão via IPv4 , utilizando TCP
            serverAddress = (self.HOST, self.PORT)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
            sock.bind(serverAddress) # vincula endereço de host e porta ao socket
            sock.listen(1) # socket entra em operação aguardando conexão de cliente, enfileirando uma conexão até que seja aceita
            print("Iniciando servidor no endereço {} porta {}...".format(self.HOST, self.PORT))
            print("")
            # aceita conexão, retorna uma tupla com um File Descriptor, usado para receber e enviar dados, e, o endereço do cliente
            conn, address = sock.accept()
            self.serverFlag = True 

        receiveThread = threading.Thread(target=self.handleReceive, args=(conn,)) # thread que manipula recebimento de mensagens

        # thread manipula envio de mensagens ao processo alvo
        sendThread = threading.Thread(target=self.sendMessage, args=(conn, TARGET_ID, TARGET_HOST))

        receiveThread.start()
        sendThread.start()

        receiveThread.join()
        sendThread.join()

        conn.close()
        sock.close() 
        self.serverFlag = False

    # conecta a servidor para envio de mensagem    
    def startClient(self, TARGET_ID, TARGET_HOST):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket IPv4, TCP/IP
        serverAddress = (TARGET_HOST, self.PORT) # define endereço alvo com host e porta
        sock.connect(serverAddress) # conecta socket ao servidor alvo

        receiveThread = threading.Thread(target=self.handleReceive, args=(sock,)) # thread que manipula recebimento de mensagens

        # thread manipula envio de mensagens ao processo alvo
        sendThread = threading.Thread(target=self.sendMessage, args=(sock, TARGET_ID, TARGET_HOST))

        receiveThread.start()
        sendThread.start()

        receiveThread.join()
        sendThread.join()

        sock.close()

    def handleReceive(self, conn):

        while(True):
        
            try:
                
                data = conn.recv(self.DATA_PAYLOAD) # recebe dados do cliente
                dataDecode = data.decode('utf-8') # decodifica dados em bytes para string
                dataJson = json.loads(dataDecode) # converte objeto string para JSON

                print("Mensagem recebida do  Processo{}".format(dataJson['senderID']))
                print("Relógio lógico atual do Processo{}: {} / Relógio lógico atual do Processo{}: {}".format(self.ID, self.getLamportClock(), dataJson['senderID'], dataJson['lamportClock']))

                self.lamportClockAlgorithm(dataJson) # executa correção de relógio lógico           
                print("Relógio lógico atualizado do Processo{}: {}".format(dataJson['receiverID'], self.getLamportClock()))
                print("===================================================================================")
                #response = self.getLamportClock()
                #conn.send(response.encode('utf-8')) # envia resposta
            except Exception as e:
                
                print("Erro ao receber mensagem: {}".format(e))
                break

    # estabelece conexão com servidor no host e porta especificados e envia mensagem
    def sendMessage(self, conn, receiverID, TARGET_HOST):

        while(True):
            try:

                self.setLamportClock(self.getLamportClock() + 1) # acrescenta evento de envio ao relógio lógico
                # dicionario que irá transmitir objeto JSON, armazena id do processo remetente, id do processo destinatário, relógio lógico de Lamport
                message = {'senderID': self.ID, 'receiverID': receiverID, 'lamportClock': self.lamportClock, 'TARGET_HOST': TARGET_HOST}
                messageStr = json.dumps(message) # serializa JSON em string
                time.sleep(self.timeRate)
                conn.send(messageStr.encode('utf-8')) # envia mensagem codificada em bytes com UTF-8 
                #response = conn.recv(self.DATA_PAYLOAD) # mensagem de resposta recebida
                
            except socket.error as e:

                print("Socket error: {}".format(str(e)))
                break
            except Exception as e:

                print("Other exception: {}".format(str(e)))
                break

# executa apenas quando chamado diretamente, evita execução quando importado por outro script
if __name__ == "__main__":

    HOSTNAME = socket.gethostname() # armazena hostname
    HOST = socket.gethostbyname(socket.gethostname()) # armazena host

    process1 = Process(0, 0, 0, False, 1, HOST, 8000, 1024) # inicializa processo
    process1.simulatesProcessExecution() # simula execução de eventos

    # constrói threads de servidor e cliente
    serverThread = threading.Thread(target=process1.openServerConnection, args=(2, '172.18.0.3',))
    clientThread = threading.Thread(target=process1.startClient, args=(2, '172.18.0.3',))

    #inicia threads
    serverThread.start()
    clientThread.start()

    serverThread.join()
    clientThread.join()


