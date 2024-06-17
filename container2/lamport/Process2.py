import random
import MessageHandler2 as messageHandler

class Process:

    def __init__(self, lamportClock, timeRate, numEvents, id):

        self.lamportClock = lamportClock # armazena contador do relógio lógico de Lamport
        self.timeRate = timeRate # taxa de tempo que cada evento consome
        self.numEvents = numEvents # número de eventos realizados pelo processo
        self.id = id # id do processo

    # simula execução do processo, definindo uma taxa aleatório de tempo para os eventos e incrementando o relógio lógico a cada evento
    def simulatesProcessExecution(self):
        
        self.timeRate = random.randint(1,3) # define a taxa de variação do tempo como um valor entre 1 e 5
        self.numEvents = random.randint(1,5) # define o número de eventos ocorridos no processo como um valor entre 1 e 10

        # atribui valor ao relógio lógico de Lamport
        for i in range(self.numEvents):
            self.lamportClock = self.lamportClock + self.timeRate

    def sendMessageForProcess1(self):

        SERVER_HOST = '172.18.0.5' # host do servidor proxy
        TARGET_HOST = '172.18.0.2' # host do servidor do processo alvo
        # dicionario que irá transmitir objeto JSON, armazena id do processo remetente, id do processo destinatário, relógio lógico de Lamport
        message = {'senderID': self.id, 'receiverID': 1, 'lamportClock': self.lamportClock, 'TARGET_HOST': TARGET_HOST} 
        newConnection = messageHandler.ClientMessageHandler(SERVER_HOST, 8000, 1024, message)
        newConnection.sendMessage()

    def getLamportClock(self):

        return self.lamportClock

    def setLamportClock(self, newLamportClock):

        self.lamportClock = newLamportClock

process2 = Process(0, 0, 0, 2)
process2.simulatesProcessExecution()
process2.sendMessageForProcess1()