import socket
import os
import hashlib
import threading

# Función para recibir archivos
def receive_file(sock, filename):
    try:
        # Enviar el nombre del archivo al servidor
        sock.sendall(filename.encode())
        filename = filename + "MB.txt"

        # Crear el directorio para guardar los archivos recibidos
        if not os.path.exists('TCP/received_files'):
            os.makedirs('TCP/received_files')

        if sock.recv(1024).decode() == "ready":
            sock.sendall("ready".encode())

        # Recibir el hash del archivo del servidor
        hash = sock.recv(1024).decode()
        print(f"Hash recibido: {hash}")

        # Recibir el archivo del servidor
        with open('TCP/received_files/' + filename, 'wb') as f:
            while True:
                data = sock.recv(1024)
                if data == b'FIN':
                    print("Archivo recibido")
                    break
                f.write(data)

        # Calcular el hash del archivo recibido
        with open('TCP/received_files/' + filename, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            print(f"Hash calculado: {file_hash}")

        # Comparar los hashes para verificar la integridad del archivo
        if hash == file_hash:
            print("El archivo recibido es íntegro")
        else:
            print("El archivo recibido está corrupto")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cerrar la conexión
        sock.close()


# Crear 25 threads para recibir archivos
threads = []
filename = input("Ingrese el nombre del archivo a recibir: ")
for i in range(25):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.20.57', 10000)
    print(f"Conectando a {server_address[0]} puerto {server_address[1]}")
    sock.connect(server_address)
    t = threading.Thread(target=receive_file, args=(sock, filename))
    threads.append(t)

# Iniciar los threads
for t in threads:
    t.start()

# Esperar a que los threads terminen
for t in threads:
    t.join()

print("Todos los archivos han sido recibidos")
