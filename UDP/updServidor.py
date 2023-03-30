# un servidor UDP simple en python
import socket
import sys
import os
import datetime
from time import time
import threading
import queue as q

server_address = ('192.168.20.60', 3400)

def send_data(sock, address, data, queue):

    #log = open(log_filename, 'w')

    # Tamaño máximo de datagrama
    max_datagram_length = 4096

    # Obtener el nombre y el tamaño del archivo
    filename = data.decode() + 'MB.txt'
    filesize = os.path.getsize('mensajes/' + filename)

    # Leer el archivo y dividirlo en datagramas
    message = open('mensajes/' + filename, 'rb').read()
    datagrams = [message[i:i + max_datagram_length] for i in range(0, len(message), max_datagram_length)]

    # Iniciar el tiempo de transferencia
    start_time = time()
    puerto_conexion = str(address[1])
    sock.sendto(puerto_conexion.encode(), address)


    # Enviar los datagramas al cliente
    for each_datagram in datagrams:
        sock.sendto(each_datagram, address)
        #print(sys.stderr, 'Enviado %s bytes de vuelta a %s' % (sent, address))

    # Envía un mensaje de finalización de transmisión
    sock.sendto(b'FIN', address)

    print(sys.stderr, 'Enviando mensaje de FIN de vuelta a ' + str(address))

    # Calcular el tiempo total de transferencia
    end_time = time()
    transfer_time = end_time - start_time

    queue.put(transfer_time)

if __name__ == '__main__':

    # Crear un socket UDP para el servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Ajustar el tamaño del buffer de recepción
    buffer_size = 65536
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)

    # Enlazar el socket al puerto
    print(sys.stderr, 'Iniciando en %s puerto %s' % server_address)
    server_socket.bind(server_address)

    # Crear un archivo de log con la fecha actual
    actual_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Crear un archivo de log con la fecha actual
    if not os.path.exists('UDP/Logs'):
        os.makedirs('UDP/Logs')    

    log_filename = 'UDP/Logs/' + actual_date + '-log.txt'
    with open(log_filename, 'w') as log:
        i = 0
        while True:

            # Esperar a recibir confirmacion de inicio de transmision
            print(sys.stderr, 'Esperando para recibir mensaje')

            # Recibir el mensaje del cliente
            client_data, client_address = server_socket.recvfrom(4096)
            
            queue = q.Queue()

            # Iniciar los threads para la transferencia de datos
            thread = threading.Thread(target=send_data, args=(server_socket, client_address, client_data, queue))
            thread.start()

            thread.join()
            transfer_time = queue.get()

            print(sys.stderr, transfer_time)

            log.write(f'[{i}], Archivo: {client_data.decode()}MB.txt, Tamaño: {os.path.getsize("mensajes/" + client_data.decode() + "MB.txt")} bytes, Tiempo de transferencia: {transfer_time} segundos\n')


            i += 1
