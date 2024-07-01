import socket
import json
import threading
import time

class Process:

    def __init__(self, ID, token, START):

        self.ID = ID # id do processo
        self.token = token # token que permite acesso ao recurso compartilhado
        self.START = START # flag marca se o processo inicia a comunicação

    def getID(self):

        return self.ID
    
    def getToken(self):

        return self.token
    
    def setToken(self, value):

        self.token = value

    def haveToken(self):

        if(self.token == True):
            return True
        else:
            return False
        
    def getStart(self):
        return self.START

   # inicia servidor e manipula recebimento de mensagem
    def serverHandler(self, HOST, PORT, DATA_PAYLOAD):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket para conexão via IPv4 , utilizando TCP
        serverAddress = (HOST, PORT) # tupla host/porta
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
        sock.bind(serverAddress) # vincula endereço de host e porta ao socket
        sock.listen(1) # socket entra em operação aguardando conexão de cliente, enfileirando uma conexão até que seja aceita
        # aceita conexão, retorna uma tupla com um File Descriptor, usado para receber e enviar dados, e, o endereço do cliente
        conn, address = sock.accept()

        while(True):
            try:
                
                data = conn.recv(DATA_PAYLOAD) # recebe dados do cliente

                self.setToken(True)
                if(self.getToken() == True):

                    self.editFile()
                
                self.setToken(False)

                #response =
                #conn.send(response.encode('utf-8')) # envia resposta

            except Exception as e:
            
                print("Erro ao receber mensagem: {}".format(e))
                break

        conn.close()
        sock.close()

    def clientHandler(self, TARGET_HOST, PORT):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket IPv4, TCP/IP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
        serverAddress = (TARGET_HOST, PORT) # define endereço alvo com host e porta
        sock.connect(serverAddress) # conecta socket ao servidor alvo

        message = {'token': self.getToken()}
        sendThread = threading.Thread(target=self.sendMessage, args=(sock,message))
        sendThread.start()
        sendThread.join()
    
        sock.close()
    
    def sendMessage(self, sock, message):

        while(True):
            if(self.getToken() == False):
                try:

                    # dicionario que irá transmitir objeto JSON, armazena id do processo remetente, id do processo destinatário, relógio lógico de Lamport
                    messageStr = json.dumps(message) # serializa JSON em string
                    sock.send(messageStr.encode('utf-8')) # envia mensagem codificada em bytes com UTF-8 
                    #response = conn.recv(DATA_PAYLOAD) # mensagem de resposta recebida
                    
                except socket.error as e:

                    print("Socket error: {}".format(str(e)))
                except Exception as e:

                    print("Other exception: {}".format(str(e)))
    
    def editFile(self):

        try:

            with open("/recursos/shared_file.txt", "a") as file:

                file.write("Processo{} editando o recurso compartilhado...\n".format(self.getID()))
                time.sleep(2)
                file.close()
        except Exception as e:

            print("Falha ao escrever no arquivo: {}".format(e))

        try:

            with open("/recursos/shared_file.txt", "r") as file:

                output = file.readline()
                print(output)
                file.close()
        except Exception as e:

            print("Falha ao ler arquivo: {}".format(e))

# executa apenas quando chamado diretamente, evita execução quando importado por outro script
if __name__ == "__main__":

    HOSTNAME = socket.gethostname() # armazena hostname
    HOST = socket.gethostbyname(socket.gethostname()) # armazena host

    process = Process(3, False, True) # inicializa processo
    
    serverThread = threading.Thread(target=process.serverHandler, args=(HOST,8000,1024))
    serverThread.start()

    if(process.getStart() == True):
        start = input("iniciar compartilhamento de recurso: ")
        if(start == "ok"):
            clientThread = threading.Thread(target=process.clientHandler, args=('172.18.0.2',8000))
            clientThread.start()

