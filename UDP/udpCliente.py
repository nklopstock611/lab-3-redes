# cliente de un servidor UPD en python
import socket
import sys
import threading

server_address = ('192.168.1.70', 3400)

def recive_data(sock, i):

    # Guardar en la carpeta ArchivosRecibidos
    file = open("UDP/ArchivosRecibidos/Cliente" + str(i) + "-Prueba-1" + ".txt", "w")
    
    # Recibir respuesta
    print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Esperando respuesta')

    data = b'data'
    while data:
        data, server = sock.recvfrom(4096)
        print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Recibido "%s"' % data)

        if data == b'FIN':
            break
        
        file.write(data.decode())

    print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Cerrando socket')
    sock.close()


if __name__ == "__main__":
    idThread = 0

    message = input('Introduce el tamaño del mensaje: ').encode()

    for i in range(0, 25):

        # Crear un socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Enviar datos
        print(sys.stderr, 'Cliente ' + str(i) + ' - ' + 'Enviando') #  % message
        sent = sock.sendto(message, server_address)

        thread = threading.Thread(target=recive_data, args=(sock, i))
        idThread += 1
        thread.start()
