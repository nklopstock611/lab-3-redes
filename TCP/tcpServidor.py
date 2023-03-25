import socket
import threading
import sys
import os
import time
import hashlib

# Define the number of clients needed before transferring files
required_clients = 2

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.20.57', 10000)
print('starting up on {} port {}'.format(*server_address))
nrTransferredFile = 0
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)

# Global variable to keep track of how many clients are ready to receive files
clients_ready = 0

def handle_connection(connection, client_address):
    global clients_ready
    try:
        print('connection from', client_address)
        # Esperar a recibir confirmacion de inicio de transmision
        print(sys.stderr, 'Esperando para recibir mensaje')
        data, address = sock.recvfrom(4096)
        data = connection.recv(16)
        # Obtener el nombre y tamaño del archivo
        filename = str(data.decode()) + 'MB.txt'
        filesize = os.path.getsize('mensajes/' + filename)
        if data:
            # Esperar a que el cliente confirme que está listo para recibir el archivo
            ready_message = connection.recv(1024).decode()
            if ready_message == "ready":
                clients_ready += 1

            # Esperar a que todos los clientes estén listos para recibir el archivo
            while clients_ready < required_clients:
                time.sleep(1)

            # Iniciar el tiempo de transferencia
            start_time = time()

            with open('mensajes/' + filename, 'rb') as f:
                offset = 0
                while offset < filesize:
                    block = data[offset:offset+1024]
                    connection.sendall(block)
                    offset += len(block)
                    print('Enviado %s bytes a %s' % (len(block), client_address))

            # Envio de hash del mensaje
            hash = hashlib.sha256(f.read()).hexdigest()
            print(f"Hash: {hash}")
            connection.sendall(hash.encode())

    finally:
        # Clean up the connection
        connection.close()

        # Reiniciar la variable de clientes listos para la próxima transferencia
        clients_ready = 0

connections = []

while len(connections) < required_clients:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    connections.append(connection)
    print(f"Connection from {client_address} accepted")

    if len(connections) == required_clients:
        for conn in connections:
            t = threading.Thread(target=handle_connection, args=(conn, client_address))
            t.start()
        connections.clear()

sock.close()

