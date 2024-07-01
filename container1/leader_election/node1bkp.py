import socket
import json
import threading
import random

class RingQueue:

    def __init__(self, nodesQueue, maxNodes, currNodes):

        self.nodesQueue = nodesQueue # fila circular de nós na rede
        self.maxNodes = maxNodes # total de nós na rede
        self.currNodes = currNodes # total de nós na fila

    # enfileira nó
    def enqueue(self, newNode):

        if(self.isQueueFull == True):
            print("Erro na inserção. A fila está cheia.")
            return
        
        self.setCurrNodes(self.getCurrNodes()+1)
        self.getNodesQueue()[self.getCurrNodes()-1] = newNode

        return self.getNodesQueue()

    # desenfileira nó
    def dequeue(self):

        node = self.getNodesQueue()[0]

        i = 0
        j = i+1
        while(j < self.getCurrNodes()):
            self.getNodesQueue()[i] = self.getNodesQueue()[j]
            i += 1
            j += 1
        
        self.setCurrNodes(self.getCurrNodes()-1)
        return node

    def getMaxNodes(self):
        return self.getMaxNodes()
    
    def setMaxNodes(self, newMaxNodes):
        self.maxNodes = newMaxNodes

    def getCurrNodes(self):
        return self.getCurrNodes()
    
    def setCurrNodes(self, newCurrNodes):
        self.currNodes = newCurrNodes

    def getNodesQueue(self):
        return self.nodesQueue
    
    def isQueueFull(self):
        if(self.getCurrNodes() >= self.getMaxNodes()):
            return True
    
#--------------------------------------------------------------------------------------------------
class Process:

    def __init__(self, ID, procStartLeaderElection, procFinishLeaderElection):

        self.ID = ID # id do processo
        self.procStartLeaderElection = procStartLeaderElection # recebe True se o processo pode iniciar a eleição de lider
        self.procFinishLeaderElection = procFinishLeaderElection # recebe True se o processo encerra a eleição de líder

    def getID(self):

        return self.ID

    def getProcStartLeaderElection(self):

        return self.procStartLeaderElection
    
    def setProcStartLeaderElection(self, newProcStartLeaderElection):

        self.procStartLeaderElection = newProcStartLeaderElection

    def getProcFinishLeaderElection(self):

        return self.procFinishLeaderElection
    
    def setProcFinishLeaderElection(self, newProcFinishLeaderElection):

        self.procFinishLeaderElection = newProcFinishLeaderElection
    
    # inicia conexões do servidor
    def openServerConnection(self, HOST, PORT, DATA_PAYLOAD, TARGET_ID, TARGET_HOST, electionQueue):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket para conexão via IPv4 , utilizando TCP
        serverAddress = (HOST, PORT) # tupla host/porta
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
        sock.bind(serverAddress) # vincula endereço de host e porta ao socket
        sock.listen(1) # socket entra em operação aguardando conexão de cliente, enfileirando uma conexão até que seja aceita
        print("Iniciando servidor no endereço {} porta {}...".format(HOST, PORT))
        print("")
        # aceita conexão, retorna uma tupla com um File Descriptor, usado para receber e enviar dados, e, o endereço do cliente
        conn, address = sock.accept()

         # thread que manipula recebimento de mensagens
        receiveThread = threading.Thread(target=self.handleReceive, args=(conn,DATA_PAYLOAD))
        # thread que manipula envio de eleição de líder       
        sendThread = threading.Thread(target=self.sendMessage, args=(conn,TARGET_ID,TARGET_HOST,DATA_PAYLOAD,electionQueue))
            
        receiveThread.start()
        sendThread.start()

        receiveThread.join()
        sendThread.join()
        
        conn.close()
        sock.close() 

    # inicia eleição de líder
    def startLeaderElection(self, TARGET_ID, TARGET_HOST, PORT, DATA_PAYLOAD, electionQueue):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket IPv4, TCP/IP
        serverAddress = (TARGET_HOST, PORT) # define endereço alvo com host e porta
        sock.connect(serverAddress) # conecta socket ao servidor alvo

        # thread que manipula recebimento de mensagens
        receiveThread = threading.Thread(target=self.handleReceive, args=(sock,DATA_PAYLOAD,)) 
        # thread que manipula envio de eleição de líder       
        sendThread = threading.Thread(target=self.sendMessage, args=(sock,TARGET_ID,TARGET_HOST,DATA_PAYLOAD, electionQueue))

        receiveThread.start()
        sendThread.start()

        receiveThread.join()
        sendThread.join()
        
        sock.close()

    def handleReceive(self, conn, DATA_PAYLOAD):

        while(True):
            try:
                
                data = conn.recv(DATA_PAYLOAD) # recebe dados do cliente
                dataDecode = data.decode('utf-8') # decodifica dados em bytes para string
                dataJson = json.loads(dataDecode) # converte objeto string para JSON

                print("Mensagem recebida do  Processo{}".format(dataJson['senderID']))
                self.setProcStartLeaderElection(True) # seta permissão para entrar na eleição de líder
                # atualiza fila de eleição de líder
                dataJson['electionQueue'] = self.buildLeaderElection(dataJson['electionQueue'])

                # verifica se a fila de eleição de líder está cheia
                if(dataJson['electionQueue'].isQueueFull() == True):
                    leader = self.finishLeaderElection(dataJson['electionQueue']) # recebe maior ID da fila
                    print(leader)

                #print("Relógio lógico atual do Processo{}: {} / Relógio lógico atual do Processo{}: {}".format(self.ID, self.getLamportClock(), dataJson['senderID'], dataJson['lamportClock']))

                #self.lamportClockAlgorithm(dataJson) # executa correção de relógio lógico           
                #print("Relógio lógico atualizado do Processo{}: {}".format(dataJson['receiverID'], self.getLamportClock()))
                #print("===================================================================================")
                #response = self.getLamportClock()
                #conn.send(response.encode('utf-8')) # envia resposta
            except Exception as e:
            
                print("Erro ao receber mensagem: {}".format(e))
                break

    # estabelece conexão com servidor no host e porta especificados e envia mensagem
    def sendMessage(self, conn, receiverID, TARGET_HOST, DATA_PAYLOAD, electionQueue):

        while(True):
            # envia mensagem apenas se já recebeu a fila de eleição de líder
            if(self.getProcStartLeaderElection() == True):
                try:

                    #self.setLamportClock(self.getLamportClock() + 1) # acrescenta evento de envio ao relógio lógico
                    # dicionario que irá transmitir objeto JSON, armazena id do processo remetente, id do processo destinatário, relógio lógico de Lamport
                    message = {'senderID': self.ID, 'electionQueue': electionQueue}
                    messageStr = json.dumps(message) # serializa JSON em string
                    conn.send(messageStr.encode('utf-8')) # envia mensagem codificada em bytes com UTF-8 
                    #response = conn.recv(DATA_PAYLOAD) # mensagem de resposta recebida
                    
                except socket.error as e:

                    print("Socket error: {}".format(str(e)))
                except Exception as e:

                    print("Other exception: {}".format(str(e)))

    # enfileira ID de processo na fila de eleição de líder        
    def buildLeaderElection(self, electionQueue):

        newQueue = electionQueue.enqueue(self.ID)
        return newQueue
    
    # retorna maior ID da fila de eleição de líder
    def finishLeaderElection(self, electionQueue):

        max = 0
        for i in electionQueue:

            if(i > max):
                max = i

        return max

# executa apenas quando chamado diretamente, evita execução quando importado por outro script
if __name__ == "__main__":

    def buildServerThread(HOST, PORT, DATA_PAYLOAD, TARGET_ID, TARGET_HOST, process, electionQueue):

        serverThread = threading.Thread(target=process.openServerConnection, args=(HOST,PORT,DATA_PAYLOAD,TARGET_ID,TARGET_HOST,electionQueue))
        serverThread.start()

    def buildClientThread(TARGET_ID, TARGET_HOST, PORT, DATA_PAYLOAD, process, electionQueue):

        clientThread = threading.Thread(target=process.startLeaderElection, args=(TARGET_ID,TARGET_HOST,PORT,DATA_PAYLOAD,electionQueue))
        clientThread.start()

    HOSTNAME = socket.gethostname() # armazena hostname
    HOST = socket.gethostbyname(socket.gethostname()) # armazena host
    electionQueue = RingQueue([0,0,0,0], 4, 0) # fila para realização da eleição de líder

    process1 = Process(1, False, False) # inicializa processo

    # constrói e inicia threads de servidor e cliente
    buildServerThread(HOST, 8000, 1024, 2,'172.18.0.3', process1, electionQueue)
    buildClientThread(2, '172.18.0.3', 8000, 1024, process1, electionQueue)


