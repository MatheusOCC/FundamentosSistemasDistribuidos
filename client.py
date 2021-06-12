#Processo cliente
  
from timeit import default_timer as timer
from dateutil import parser
import threading
import datetime
import socket 
import time
  
  
# função de thread do cliente usada para enviar Horário no lado do cliente
def startSendingTime(slave_client):
  
    while True:
        # fornece ao servidor a hora do relógio no cliente
        slave_client.send(str(
                       datetime.datetime.now()).encode())
  
        print("Horário recente enviado com sucesso",
                                          end = "\n\n")
        time.sleep(5)
  
  
# função de thread do cliente usada para receber Horário do lado do servidor
def startReceivingTime(slave_client):
  
    while True:
        # recebe dados do servidor
        Synchronized_time = parser.parse(
                          slave_client.recv(1024).decode())
  
        print("O Horário sincronizado do cliente é: " + \
                                    str(Synchronized_time),
                                    end = "\n\n")
  
  
# função usada para sincronizar o tempo de processo do cliente
def initiateSlaveClient(port = 5000):
  
    slave_client = socket.socket()          
        
    # conecta ao servidor de relógio no computador local
    slave_client.connect(('127.0.0.1', port)) 
  
    # começa a enviar tempo para o servidor
    print("Começando a receber tempo do servidor\n")
    send_time_thread = threading.Thread(
                      target = startSendingTime,
                      args = (slave_client, ))
    send_time_thread.start()
  
  
    # começa a receber o horário sincronizado do servidor
    print("Começando a receber " + \
                         "tempo sincronizado do servidor\n")
    receive_time_thread = threading.Thread(
                       target = startReceivingTime,
                       args = (slave_client, ))
    receive_time_thread.start()
  
  
# função de Driver
if __name__ == '__main__':
  
    # inicializa o Slave / Cliente
    initiateSlaveClient(port = 5000)
