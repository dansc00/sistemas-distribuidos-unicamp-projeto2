import os
import sys
import socket
import json
import threading
import random
import time

class Queue:

    def __init__(self, nodesQueue, maxNodes, currNodes):
        self.nodesQueue = nodesQueue # fila de nós na rede
        self.maxNodes = maxNodes # total de nós na rede
        self.currNodes = currNodes # total de nós na fila

    # enfileira nó
    def enqueue(self, newNode):
        if(self.isQueueFull() == True):
            print("Insertion error. The queue is full.")
            sys.exit(1)
        
        self.nodesQueue[self.currNodes] = newNode
        self.currNodes = self.currNodes + 1
        
        return self

    # desenfileira nó
    def dequeue(self):
        node = self.nodesQueue[0]

        i = 0
        j = i+1
        while(j < self.currNodes):
            self.nodesQueue[i] = self.nodesQueue[j]
            i += 1
            j += 1
        
        self.currNodes = self.currNodes - 1
        return node

    def getMaxNodes(self):
        return self.maxNodes
    
    def setMaxNodes(self, newMaxNodes):
        self.maxNodes = newMaxNodes

    def getCurrNodes(self):
        return self.currNodes
    
    def setCurrNodes(self, newCurrNodes):
        self.currNodes = newCurrNodes

    def getNodesQueue(self):
        return self.nodesQueue
    
    def isQueueFull(self):
        if(self.currNodes >= self.maxNodes):
            return True
        
    # converte objeto em dicionário    
    def toDict(self):
        return self.__dict__
    
    # serializa JSON. Converte dicionário em string JSON
    def toJson(self):
        return json.dumps(self.toDict())
    
    @classmethod # método da classe
    #desempacota para atributos da classe. Converte dicionário em objeto
    def argumentUnpacking(cls, dict):
        return cls(**dict)
    
    @classmethod # método da classe
    # desserializa JSON. Converte string JSON em objeto
    def fromJson(cls, stringJson):
        dict = json.loads(stringJson)
        return cls.argumentUnpacking(dict)
    
#--------------------------------------------------------------------------------------------------
class Process:

    def __init__(self, ID, toStartLeaderElection, toFinishLeaderElection):
        self.ID = ID # id do processo
        self.toStartLeaderElection = toStartLeaderElection # recebe True se o processo inicia a eleição de lider
        self.toFinishLeaderElection = toFinishLeaderElection # recebe True se o processo encerra a eleição de líder

    def getID(self):
        return self.ID

    def getToStartLeaderElection(self):
        return self.toStartLeaderElection
    
    def setToStartLeaderElection(self, value):
        self.toStartLeaderElection = value

    def getToFinishLeaderElection(self):
        return self.toFinishLeaderElection
    
    def setToFinishLeaderElection(self, value):
        self.toFinishLeaderElection = value
    
    # inicia servidor e manipula recebimento de mensagem
    def serverHandler(self, HOST, PORT, TARGET_PORT, DATA_PAYLOAD, TARGET_HOST):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket para conexão via IPv4 , utilizando TCP
        serverAddress = (HOST, PORT) # tupla host/porta
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
        sock.bind(serverAddress) # vincula endereço de host e porta ao socket
        sock.listen(1) # socket entra em operação aguardando conexão de cliente, enfileirando uma conexão até que seja aceita
        
        print(f"Server listening on {HOST}:{PORT}...")
        print("")
        
        while(True):
            # aceita conexão, retorna uma tupla com um File Descriptor, usado para receber e enviar dados, e, o endereço do cliente
            conn, address = sock.accept()

            try:
                data = conn.recv(DATA_PAYLOAD) # recebe dados do cliente
                dataDecode = data.decode('utf-8') # decodifica dados em bytes para string
                dataJson = json.loads(dataDecode) # converte objeto string para JSON

                print(f"Received message from Process{dataJson['senderID']}")
                # encerra eleição de líder
                if(self.getToFinishLeaderElection() == True):
                    print("End of the leader election")
                    break

                if(dataJson['isLeaderElected'] == False):
                    electionQueue = Queue.fromJson(dataJson['electionQueue']) # converte string JSON em objeto
                    print(f"Current election queue: {electionQueue.getNodesQueue()}")

                    # atualiza fila de eleição de líder
                    newQueue = self.buildLeaderElection(electionQueue) # enfileira ID

                    # verifica se a fila de eleição de líder está cheia
                    if(newQueue.isQueueFull() == True):
                        # encerra eleição e inicia compartilhamento de lider
                        print(f"Last election queue: {newQueue.getNodesQueue()}")
                        leader = self.finishLeaderElection(newQueue) # recebe maior ID da fila
                        print(f"Elected leader ID: {leader}")
                        self.setToFinishLeaderElection(True)
                        self.shareLeader(TARGET_HOST, TARGET_PORT, DATA_PAYLOAD, leader)
                    else:
                        # repassa fila de eleição
                        newQueue = newQueue.toJson() # converte objeto em string JSON
                        message = {'senderID': self.ID, 'electionQueue': newQueue, 'isLeaderElected': False}
                        self.sendMessage(TARGET_HOST, TARGET_PORT, DATA_PAYLOAD, message)
                else:
                    print(f"Leader succesfully passed on. Leader is {dataJson['leader']}")
                    self.shareLeader(TARGET_HOST, TARGET_PORT, DATA_PAYLOAD, dataJson['leader'])

                #response =
                #conn.send(response.encode('utf-8')) # envia resposta

            except Exception as e:
                print(f"Receiving message error: {e}")
                break

            finally:
                conn.close()

        sock.close()

    # envia mensagem
    def sendMessage(self, TARGET_HOST, PORT, DATA_PAYLOAD, message):
        retries = 5      
        for i in range(retries):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket IPv4, TCP/IP
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
                serverAddress = (TARGET_HOST, PORT) # define endereço alvo com host e porta
                sock.connect(serverAddress) # conecta socket ao servidor alvo

                # dicionario que irá transmitir objeto JSON, armazena id do processo remetente, id do processo destinatário, relógio lógico de Lamport
                messageStr = json.dumps(message) # serializa JSON em string
                time.sleep(1)
                sock.send(messageStr.encode('utf-8')) # envia mensagem codificada em bytes com UTF-8 
                sock.close()
                break  
                
            except Exception as e:
                print(f"{e}: Connection failed. Retrying after 5 seconds...")
                time.sleep(5)
                continue
    
    # inicia eleição de líder
    def startLeaderElection(self, TARGET_HOST, PORT, DATA_PAYLOAD, electionQueue):
        electionQueue = electionQueue.toJson() # converte objeto em string JSON
        # id do remetente , fila de eleição, flag para fim da eleição de líder
        message = {'senderID': self.ID, 'electionQueue': electionQueue, 'isLeaderElected': False}

        self.sendMessage(TARGET_HOST, PORT, DATA_PAYLOAD, message)

    # enfileira ID de processo na fila de eleição de líder        
    def buildLeaderElection(self, electionQueue):
        newQueue = electionQueue.enqueue(self.getID())
        return newQueue
    
    # retorna maior ID da fila de eleição de líder
    def finishLeaderElection(self, electionQueue):
        max = 0
        for i in electionQueue.getNodesQueue():
            if(i > max):
                max = i

        return max
    
    # repassa lider eleito para nós na rede
    def shareLeader(self, TARGET_HOST, PORT, DATA_PAYLOAD, leader):
        message = {'senderID': self.ID, 'leader': leader, 'isLeaderElected': True}
        self.sendMessage(TARGET_HOST, PORT, DATA_PAYLOAD, message)

# executa apenas quando chamado diretamente, evita execução quando importado por outro script
if __name__ == "__main__":

    HOSTNAME = socket.gethostname() # armazena hostname
    HOST = socket.gethostbyname(socket.gethostname()) # armazena host
    NODE2_IPV4 = os.getenv("NODE2_IPV4") # ipv4 do node2
    CONNECTION_PORT = int(os.getenv("CONNECTION_PORT")) # porta de conexão
    electionQueue = Queue([0,0,0,], 3, 0) # fila para realização da eleição de líder

    ID = random.randint(1,100) # id entre 1 e 100
    process = Process(ID, True, False) # inicializa processo

    # constrói e inicia threads de servidor e cliente
    serverThread = threading.Thread(target=process.serverHandler, args=(HOST,CONNECTION_PORT,8002,1024,NODE2_IPV4))
    serverThread.start()

    if(process.getToStartLeaderElection() == True):
        print("Starting leader election...")
        clientThread = threading.Thread(target=process.startLeaderElection, args=(NODE2_IPV4,8002,1024,electionQueue))
        clientThread.start()
    
    serverThread.join()


