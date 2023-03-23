# un servidor UDP simple en python
import socket
import sys

# Crear un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

buffer_size = 8192
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)

# Enlazar el socket al puerto
server_address = ('192.168.1.70', 3400)

print(sys.stderr, 'Iniciando en %s puerto %s' % server_address)
sock.bind(server_address)

max_datagram_length = 4096

while True:
    # Esperar a recibir confirmacion de inicio de transmision
    print(sys.stderr, 'Esperando para recibir mensaje')
    data, address = sock.recvfrom(4096)

    if data:
        message = open('mensajes/' + str(data.decode()) + 'MB.txt', 'rb').read()
        datagrams = [message[i:i + max_datagram_length] for i in range(0, len(message), max_datagram_length)]
        
        # Enviar datos pedidos de vuelta al cliente
        for each_datagram in datagrams:
            sent = sock.sendto(each_datagram, address)
            print(sys.stderr, 'Enviado %s bytes de vuelta a %s' % (sent, address))

        # Envía un mensaje de finalización de transmisión
        sent = sock.sendto(b'FIN', address)
        print(sys.stderr, 'Enviando mensaje de FIN de vuelta a ' + str(address))
        