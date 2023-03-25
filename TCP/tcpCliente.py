import socket
import os
import datetime

# Crear un socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket al puerto
server_address = ('127.0.0.1', 3400)

# Obtener la fecha y hora actual para el nombre del archivo de registro
actual_date = datetime.datetime.now().strftime("%Y-%m-%d%H-%M-%S")

print('Iniciando en %s puerto %s' % server_address)
sock.bind(server_address)

# Escuchar conexiones entrantes
sock.listen(5)

max_buffer_size = 4096

with open('TCP/Logs/' + actual_date + '-log.txt', 'w') as log:

    while True:
        # Esperar a recibir una conexión
        print('Esperando para recibir conexión')
        connection, client_address = sock.accept()

        try:
            print('Conexión desde', client_address)

            # Recibir el nombre del archivo a enviar
            data = connection.recv(max_buffer_size)

            if data:
                # Obtener el nombre y tamaño del archivo
                filename = str(data.decode()) + 'MB.txt'
                filesize = os.path.getsize('mensajes/' + filename)

                # Iniciar el tiempo de transferencia
                start_time = datetime.datetime.now()

                # Abrir el archivo y enviarlo en bloques
                with open('mensajes/' + filename, 'rb') as f:
                    while True:
                        block = f.read(max_buffer_size)
                        if not block:
                            break
                        connection.sendall(block)
                        print('Enviado %s bytes a %s' % (len(block), client_address))

                # Envía un mensaje de finalización de transmisión
                connection.sendall(b'FIN')
                print('Enviando mensaje de FIN a ' + str(client_address))

                # Calcular el tiempo total de transferencia
                end_time = datetime.datetime.now()
                total_time = (end_time - start_time).total_seconds()

                # Escribir en el archivo de registro
                log.write(f'Archivo enviado: {filename}, tamaño: {filesize} bytes, tiempo de transferencia: {total_time:.3f} segundos\n')

        finally:
            # Cerrar la conexión
            connection.close()
