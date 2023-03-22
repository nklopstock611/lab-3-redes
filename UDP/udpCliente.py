# cliente de un servidor UPD en python
import socket
import sys

# Crear un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = b'LAPOO'

try:
        # Enviar datos
        print(sys.stderr, 'Enviando "%s"' % message)
        sent = sock.sendto(message, server_address)
    
        # Recibir respuesta
        print(sys.stderr, 'Esperando respuesta')
        data, server = sock.recvfrom(4096)
        print(sys.stderr, 'Recibido "%s"' % data)

finally:
        print(sys.stderr, 'Cerrando socket')
        sock.close()