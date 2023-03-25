import socket
import os
import hashlib

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket al puerto del servidor
server_address = ('localhost', 10000)
print('Conectando a {} puerto {}'.format(*server_address))
sock.connect(server_address)

# Pedir al usuario que ingrese el nombre del archivo a recibir
filename = input("Ingrese el nombre del archivo a recibir: ")

try:
    # Enviar el nombre del archivo al servidor
    sock.sendall(filename.encode())
    filename = filename + "MB.txt"
    # Crear el directorio para guardar los archivos recibidos
    if not os.path.exists('received_files'):
        os.makedirs('received_files')
    if sock.recv(1024).decode() == "ready":
        sock.sendall("ready".encode())
        
    
     # Recibir el hash del archivo del servidor
    hash = sock.recv(1024).decode()
    print(f"Hash recibido: {hash}")

    # Recibir el archivo del servidor
    with open('received_files/' + filename, 'wb') as f:
        while True:
            data = sock.recv(1024)
            if data == b'FIN':
                print("Archivo recibido")
                break
            f.write(data)
            


    # Calcular el hash del archivo recibido
    with open('received_files/' + filename, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
        print(f"Hash calculado: {file_hash}")

    # Comparar los hashes para verificar la integridad del archivo
    if hash == file_hash:
        print("El archivo recibido es íntegro")
    else:
        print("El archivo recibido está corrupto")

finally:
    # Cerrar la conexión
    sock.close()
