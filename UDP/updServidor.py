# un servidor UDP simple en python
import socket
import sys

# Crear un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enlazar el socket al puerto
server_address = ('localhost', 3400)

print(sys.stderr, 'Iniciando en %s puerto %s' % server_address)
sock.bind(server_address)

while True:
    # Esperar a recibir datos
    print(sys.stderr, 'Esperando para recibir mensaje')
    data, address = sock.recvfrom(4096)
    
    # Imprimir datos recibidos
    print(sys.stderr, 'Recibido %s bytes de %s' % (len(data), address))
    print(sys.stderr, data)
    
    # Comprobar si es necesario responder
    if data:
        # Enviar datos de vuelta al cliente
        data = b'RECIBIDO'
        sent = sock.sendto(data, address)
        print(sys.stderr, 'Enviado %s bytes de vuelta a %s' % (sent, address))
        
