# cliente de un servidor UPD en python
import socket
import sys

# Crear un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# buf_size = 8192
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buf_size)

server_address = ('192.168.1.70', 3400)

max_datagram_length = 512

message_length = input('Introduce el tamaño del mensaje: ')
message = open('mensajes/' + str(message_length) + 'MB.txt').read().encode()

datagrams = [message[i:i + max_datagram_length] for i in range(0, len(message), max_datagram_length)]

try:
        for each_datagram in datagrams:
                # Enviar datos
                print(sys.stderr, 'Enviando') #  % message
                sent = sock.sendto(message, server_address)
        
                # Recibir respuesta
                print(sys.stderr, 'Esperando respuesta')
                data, server = sock.recvfrom(4096)
                print(sys.stderr, 'Recibido "%s"' % data)

finally:
        print(sys.stderr, 'Cerrando socket')
        sock.close()