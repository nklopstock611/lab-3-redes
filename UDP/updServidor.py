# cliente de un servidor UPD en python
import socket
import sys

# Crear un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 3400)

size = input("Introduce el tamaño del mensaje: ")
message = open("mensajes/" + size + "MB.txt", "r").read().encode()

max_datagram_length = 1024
datagrams = [message[i:i+max_datagram_length] for i in range(0, len(message), max_datagram_length)]

try:
        for each_datagram in datagrams:
                # Enviar datos
                print(sys.stderr, 'Enviando "%s"' % each_datagram)
                sent = sock.sendto(message, server_address)
        
                # Recibir respuesta
                print(sys.stderr, 'Esperando respuesta')
                data, server = sock.recvfrom(4096)
                print(sys.stderr, 'Recibido "%s"' % data)

finally:
        print(sys.stderr, 'Cerrando socket')
        sock.close()
