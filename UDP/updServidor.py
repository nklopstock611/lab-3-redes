# un servidor UDP simple en python
import socket
import sys
import os
import datetime
from time import time

# Crear un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

buffer_size = 8192
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)

# Enlazar el socket al puerto
server_address = ('192.168.1.70', 3400)

# Obtener la fecha y hora actual para el nombre del archivo de registro
actual_date = datetime.datetime.now().strftime("%Y-%m-%d%H-%M-%S")

print(sys.stderr, 'Iniciando en %s puerto %s' % server_address)
sock.bind(server_address)

max_datagram_length = 4096

nrTransferredFile = 0

with open('UDP/Logs/' + actual_date + '-log.txt', 'w') as log:

    while True:

        # Esperar a recibir confirmacion de inicio de transmision
        print(sys.stderr, 'Esperando para recibir mensaje')
        data, address = sock.recvfrom(4096)

        nrTransferredFile += 1

        if data:

            # Obtener el nombre y tamaño del archivo
            filename = str(data.decode()) + 'MB.txt'
            filesize = os.path.getsize('mensajes/' + filename)

            # Iniciar el tiempo de transferencia
            start_time = time()

            # Leer el archivo y dividirlo en datagramas
            message = open('mensajes/' + filename, 'rb').read()
            datagrams = [message[i:i + max_datagram_length] for i in range(0, len(message), max_datagram_length)]

            # Enviar los datagramas al cliente
            for each_datagram in datagrams:
                sent = sock.sendto(each_datagram, address)
                print(sys.stderr, 'Enviado %s bytes de vuelta a %s' % (sent, address))

            # Envía un mensaje de finalización de transmisión
            sent = sock.sendto(b'FIN', address)
            print(sys.stderr, 'Enviando mensaje de FIN de vuelta a ' + str(address))

            # Calcular el tiempo total de transferencia
            end_time = time()
            total_time = end_time - start_time

            # Escribir en el archivo de registro
            log.write(f'[{nrTransferredFile}], Archivo enviado: {filename}, tamaño: {filesize} bytes, tiempo de transferencia: {total_time:.3f} segundos\n')
