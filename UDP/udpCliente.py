# cliente de un servidor UPD en python
import os
import socket
import sys
import threading
import datetime
from time import time

server_address = ('192.168.1.70', 3400)

def recive_data(sock, i):

    # Guardar en la carpeta ArchivosRecibidos
    file = open("UDP/ArchivosRecibidos/Cliente" + str(i) + "-Prueba-1" + ".txt", "w")
    
    # Recibir respuesta
    print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Esperando respuesta')

    data = b'data'
    while data:
        data, server = sock.recvfrom(4096)
        if data == b'FIN':
            print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Recibido "%s"' % data)
            break
        
        file.write(data.decode())

    print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Cerrando socket ' + str(i))
    sock.close()


if __name__ == "__main__":

    idThread = 0

    init_message = input('Introduce el tamaño del mensaje: ').encode()
    sec_message = input('Introduce el número de clientes: ')

    # Obtener la fecha y hora actual para el nombre del archivo de logs
    actual_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    for i in range(0, int(sec_message)):

        # Crear un socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Ajustar el tamaño del buffer de recepción
        buffer_size = 65536
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)

        # Iniciar el tiempo de transferencia
        start_time = time()

        # Enviar datos
        print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Enviando') #  % message
        sent = sock.sendto(init_message, server_address)

        thread = threading.Thread(target=recive_data, args=(sock, i))
        idThread += 1
        thread.start()

        # Calcular el tiempo total de transferencia
        end_time = time()
        total_time = end_time - start_time

    log = open('UDP/Logs/' + actual_date + '-log.txt', 'w')        
    
    thread.join()
    for i in range(0, int(sec_message)):

        # Verificación correctitud del archivo recibido
        filesize = os.path.getsize('UDP/ArchivosRecibidos/Cliente' + str(i) + '-Prueba-1' + '.txt')
        
        success = 'Error en transferencia (el archivo no se recibió completo)'
        if filesize == int(init_message.decode()) * 1048576:
            success = 'Transferencia exitosa'

        log.write(f'[Cliente {i}], {success} ({filesize} bytes vs {int(init_message.decode()) * 1048576}), Tiempo: {total_time} segundos\n')
  