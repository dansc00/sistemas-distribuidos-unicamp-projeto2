import socket
import random

class ClientConnection:

    def __init__(self, HOST, PORT, DATA_PAYLOAD):

        self.HOST = HOST # ip do servidor
        self.PORT = PORT # porta para conexão
        self.DATA_PAYLOAD = DATA_PAYLOAD # tamanho máximo possível para transmissão de dados	

    def initiateConnection(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket IPv4, TCP/IP
        print("Conectando ao endereço %s porta %s" %(self.HOST, self.PORT))
        serverAddress = (self.HOST, self.PORT)
        sock.connect(serverAddress) # conecta socket ao servidor
        try:
            message = "Teste"
            print("Enviando %s" %message)
            sock.send(message.encode('utf-8')) # envia dados codificados em string
            data = sock.recv(self.DATA_PAYLOAD)
            print("Recebido: %s" %data)
        except socket.error as e:
            print("Socket error: %s" %str(e))
        except Exception as e:
            print("Other exception: %s" %str(e))
        finally:
            print("Closing connection")
            sock.close()

def main():

    HOST = "172.18.0.2"
    newConnection = ClientConnection(HOST, 8000, 1024)
    newConnection.initiateConnection()

main()