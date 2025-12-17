import os
import socket
import threading
import json
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
    def serverHandler(self, HOST, PORT, TARGET_PORT, DATA_PAYLOAD, TARGET_HOST):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket para conexão via IPv4 , utilizando TCP
        serverAddress = (HOST, PORT) # tupla host/porta
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
        sock.bind(serverAddress) # vincula endereço de host e porta ao socket
        sock.listen(1) # socket entra em operação aguardando conexão de cliente, enfileirando uma conexão até que seja aceita
        print(f"Server listening on {HOST}:{PORT}...")
        print("")

        while(True):
            try:
                # aceita conexão, retorna uma tupla com um File Descriptor, usado para receber e enviar dados, e, o endereço do cliente
                conn, address = sock.accept()
                data = conn.recv(DATA_PAYLOAD).decode('utf-8') # recebe dados do cliente
                dataJson = json.loads(data)

                self.setToken(True) # seta token para permitir acesso ao recurso
                if(self.getToken() == True):

                    self.editFile() # simula acesso ao recurso
                
                self.setToken(False) # seta token para retirar permissão de acesso ao recurso
                self.sendMessage(TARGET_HOST, TARGET_PORT) # repassa token
                #response =
                #conn.send(response.encode('utf-8')) # envia resposta

            except Exception as e:
                print(f"Receiving message error: {e}")
                break

        conn.close()
        sock.close()
    
    # envia mensagem
    def sendMessage(self, TARGET_HOST, PORT):
        
        retries = 5
        message = {'senderID': self.getID(), 'token': 'token'} # mensagem que representa o token
        
        for i in range(retries):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket IPv4, TCP/IP
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite reutilização do endereço host/port
                serverAddress = (TARGET_HOST, PORT) # define endereço alvo com host e porta
                sock.connect(serverAddress) # conecta socket ao servidor alvo

                messageStr = json.dumps(message)
                sock.send(messageStr.encode('utf-8')) # envia mensagem codificada em bytes com UTF-8 
                sock.close()
                break  
                
            except Exception as e:
                print(f"{e}: Connection failed. Retrying after 5 seconds..")
                time.sleep(5)
                continue
    
    # simula acesso ao recurso compartilhado
    def editFile(self):
        try:
            # escreve no arquivo (cria se não existir)
            with open("/resources/shared_file.txt", "a+") as file:
                print(f"Process{self.getID()} is editing the shared file...")
                file.write(f"Process{self.getID()} is editing the shared file...\n")
                
        except Exception as e:
            print(f"Write file error: {e}")

        time.sleep(1)

# executa apenas quando chamado diretamente, evita execução quando importado por outro script
if __name__ == "__main__":

    HOSTNAME = socket.gethostname() # armazena hostname
    HOST = socket.gethostbyname(socket.gethostname()) # armazena host
    NODE2_IPV4 = os.getenv("NODE2_IPV4") # próximo nó no anel
    CONNECTION_PORT = int(os.getenv("CONNECTION_PORT"))

    process = Process(1, True, True) # inicializa processo com token (nó inicial)
    
    print(f"Starting mutex server on {HOST}:{CONNECTION_PORT}...")
    serverThread = threading.Thread(target=process.serverHandler, args=(HOST,CONNECTION_PORT,8002,1024,NODE2_IPV4))
    serverThread.start()
    
    if(process.getStart() == True):
        print("Initiating token circulation...")
        clientThread = threading.Thread(target=process.sendMessage, args=(NODE2_IPV4,8002))
        clientThread.start()

    serverThread.join()