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
        #print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Recibido "%s"' % data)
        #print(sys.stderr, 'Cliente ' + str(i) + ' - Recibió')
        if data == b'FIN':
            print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Recibido "%s"' % data)
            break
        
        file.write(data.decode())

    print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Cerrando socket ' + str(i))
    sock.close()


if __name__ == "__main__":

    idThread = 0

    message = input('Introduce el tamaño del mensaje: ').encode()

    # Obtener la fecha y hora actual para el nombre del archivo de logs
    actual_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    for i in range(0, 25):

        # Crear un socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Iniciar el tiempo de transferencia
        start_time = time()

        # Enviar datos
        print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Enviando') #  % message
        sent = sock.sendto(message, server_address)

        thread = threading.Thread(target=recive_data, args=(sock, i))
        idThread += 1
        thread.start()

        # Calcular el tiempo total de transferencia
        end_time = time()
        total_time = end_time - start_time


    # print('LAPOOOOOOOOOO')
    # for i in range(0, 25):
    #     thread.join()

    # with open('UDP/Logs/' + actual_date + '-log.txt', 'w') as log:
        
    #     for i in range(0, 25):

    #         # Verificación correctitud del archivo recibido
    #         filesize = os.path.getsize('UDP/ArchivosRecibidos/Cliente' + str(i) + '-Prueba-1' + '.txt')

    #         success = 'Error en transferencia (el archivo no se recibió completo)'
    #         if filesize == int(message):
    #             success = 'Transferencia exitosa'

    #         log.write(f'[Cliente {i}], {success}, Tiempo: {total_time} segundos\n')
