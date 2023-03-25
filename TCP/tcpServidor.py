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
server_address = ('192.168.20.57', 30000)
print('starting up on {} port {}'.format(*server_address))
nrTransferredFile = 0
sock.bind(server_address)

# Listen for incoming connections
sock.listen(3)

# Global variable to keep track of how many clients are ready to receive files
clients_ready = 0

def handle_connection(connection, client_address):
    global clients_ready
    try:
        print('connection from', client_address)
        # Esperar a recibir confirmacion de inicio de transmision
        print(sys.stderr, 'Esperando para recibir mensaje')
        data = connection.recv(16)
        # Obtener el nombre y tamaño del archivo
        filename = str(data.decode()) + 'MB.txt'

        connection.sendall("ready".encode())

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
            start_time = time.time()

            # Envio de hash del mensaje
            file_hash = hashlib.sha256(open('mensajes/' + filename, 'rb').read()).hexdigest()
            connection.sendall(file_hash.encode())
            
            print(f"Enviando archivo {filename} a {client_address}")
            with open('mensajes/' + filename, 'rb') as f:
                offset = 0
                while offset < filesize:
                    # Leer el archivo en bloques de 1024 bytes
                    data = f.read(1024)
                    # Enviar el bloque al cliente
                    connection.sendall(data)
                    offset += len(data) 
                    
            # Enviar confirmación de archivo enviado
            connection.sendall("FIN".encode())
            print(f"Archivo enviado a {client_address}")
            # Calcular el tiempo de transferencia
            end_time = time.time()
            transfer_time = end_time - start_time
            print(f"Tiempo de transferencia: {transfer_time} segundos")
            print(f"Velocidad de transferencia: {filesize / transfer_time} bytes/segundo")

    finally:
        # Clean up the connection
        connection.close()
        

connections = []

while len(connections) < required_clients:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    
    print(f"Connection from {client_address} accepted")
    t = threading.Thread(target=handle_connection, args=(connection, client_address))
    connections.append(t)

# Esperar a que los threads terminen
for t in connections:
    t.start()

for t in connections:
    t.join()
# Cerrar la conexión

sock.close()


