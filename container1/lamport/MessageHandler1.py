import socket
import json

class ClientMessageHandler:

    def __init__(self, SERVER_HOST, PORT, DATA_PAYLOAD, message):

        self.SERVER_HOST = SERVER_HOST # ip do servidor
        self.PORT = PORT # porta para conexão
        self.DATA_PAYLOAD = DATA_PAYLOAD # tamanho máximo possível para transmissão de dados
        self.message = message # mensagem a ser enviada ao processo alvo

    # estabelece conexão com servidor no host e porta especificados
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