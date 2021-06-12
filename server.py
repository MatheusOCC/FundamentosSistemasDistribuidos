# ###################################################################### #
# Atividade de implementação de Código                                   #
# Disciplina: Fundamentos de Sistemas Distribuídos                       #
# Professores: Alirio e Macedo                                           #
# Alunos: Ezequias, Matheus e Luis Otavio                                #
# Objetivo: sincronização de relógios                                    #
#                                                                        #
# Descrição: Os processos começam suas execuções a                       #
# partir de acesso ao tempo fornecido pelo NTP.                          #
# Em cada rodada de sincronização, os processos executam                 #
# o algoritmo de Berkeley para sincronização interna de                  #
# seus relógios. Nova sincronização externa com NTP deve                 #
# ser realização se a diferença entre o tempo interno                    #
# sincronizado e NTP for maior que um parâmetro K, que                   #
# deve ser definido no início da execução. Cada processo                 #
# deve mostrar na tela o valor do relógio local em cada                  #
# ponto de sincronização, antes de depois do ajuste.                     #
#                                                                        #
# Identificação: Socket_Server                                           #
# Arquivo: t_server.py                                                   #
# Fonte: Harshit Saini (Autor)                                           #
# https://www.geeksforgeeks.org/berkeleys-algorithm/                     #
# ###################################################################### #

# Servidor de relógio mestre.

## Bibliotecas de funções Python3 para a construção de um servidor de relógio
from functools import reduce              # biblioteca reduce para realizar uma soma de uma lista de valores
from dateutil import parser               # 
import threading
import datetime
import socket
import time

## infra-estrutura de dados utilizada para armazenar
#o endereço do cliente e os dados do relógio
client_data = {}

'''Função nested thread utilizado para receber 
    tempo de relógio de um cliente ligado'''

def startRecieveingClockTime ( connector , address ) :
    while True :
        # receber hora do relógio
        clock_time_string = connector.recv ( 1024 ).decode ( )
        clock_time = parser.parse ( clock_time_string )
        clock_time_diff = datetime.datetime.now ( ) - \
                                                 clock_time

        client_data[address] = {
                       "clock_time"      : clock_time ,
                       "time_difference" : clock_time_diff ,
                       "connector"       : connector
                       }
        
        print ( "Client Data updated with: " + str(address) ,
                                              end = "\n\n")
        time.sleep ( 5 )

'''função master thread utilizada para abrir o portal para
   aceitar clientes em determinado porto'''
def startConnecting ( master_server ) :
    
    # busca o tempo do relógio aos escravos / clientes
    while True :
        # aceitar um cliente / cliente de relógio escravo
        master_slave_connector , addr = master_server.accept ( )
        slave_address = str ( addr [ 0 ] ) + ":" + str ( addr [ 1 ] )
    

        print ( slave_address + " foi conectado com sucesso" )

        current_thread = threading.Thread (
                         target = startRecieveingClockTime ,
                         args = ( master_slave_connector ,
                                           slave_address , ) )
        current_thread.start ( )
  
# função subroutine utilizada para obter a diferença média do relógio
def getAverageClockDiff ( ) :
    current_client_data = client_data.copy ( )

    time_difference_list = list ( client [ 'time_difference' ] 
                                for client_addr , client 
                                    in client_data.items ( ) )

    
    sum_of_clock_difference = sum ( time_difference_list , \
                                   datetime.timedelta ( 0 , 0 ) )

    average_clock_difference = sum_of_clock_difference \
                                         / len ( client_data )

    return  average_clock_difference

''' função master sync thread utilizada para gerar
    ciclos de sincronização do relógio na rede'''
def synchronizeAllClocks ( ) :

    while True :

        print ( "New synchroniztion cycle started." )
        print( "Number of clients to be synchronized: " , str ( len ( client_data ) ) )

        if len ( client_data ) > 0 :

            average_clock_difference = getAverageClockDiff ( )

            for client_addr , client in client_data.items ( ) :
                try :
                    synchronized_time = datetime.datetime.now ( ) + average_clock_difference
                    client [ 'connector' ].send ( str ( synchronized_time ).encode ( ) )

                except Exception as e:
                     print ( "Something went wrong while sending synchronized time through " , str ( client_addr ) )

        else:
            print ( "No client data. Synchronization not applicable." )

        print ( "\n\n" )
        time.sleep ( 5 )

#Função utilizada para iniciar o Servidor Relógio / Nó Mestre
def initiateClockServer ( port = 5000 ) :
  
    master_server = socket.socket ( )
    master_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
    print ( "Socket at master node created successfully\n" )
        
    master_server.bind ( ( '' , port ) )
  
    # inicia a lista para solicitação
    master_server.listen ( 10 )
    print ( "Clock server started...\n" )
  
    # iniciar  connections
    print ( "Starting to make connections...\n" )
    master_thread = threading.Thread ( target = startConnecting , args = ( master_server , ) )
    master_thread.start ( )
  
    # start synchroniztion
    print ( "Starting synchronization parallely...\n" )
    sync_thread = threading.Thread ( target = synchronizeAllClocks , args = ( ) )
    sync_thread.start ( )

# Driver function
if __name__ == '__main__' :
  
    #  Acionar o Servidor do Relógio
    initiateClockServer ( port = 5000 )
