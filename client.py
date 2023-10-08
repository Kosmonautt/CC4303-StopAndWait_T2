import socket
import sys
import aux 

# socket no orientado a conexión
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# tamaño del buffer (16 bytes)
buff_size = 16

# se consigue el nombre del archivo que se quiere enviar
dir = sys.argv[1]
# se abre el archivo
f = open(dir, "r")
# se guarda el mensaje
mssg = f.read()
# se pasa a bytes
mssg = mssg.encode()
# largo del mensaje en bytes
len_mssg = len(mssg)

# puerto usado para la comunicación
port = 8000
# dirección hacia donde se envía el mensaje
server_address = ('localhost',port)

# bytes enviados
bytes_sent = 0

while bytes_sent < len_mssg:
    # máximo bytes hasta el que se va a enviar
    max_byte = min(len_mssg, bytes_sent + buff_size)

    # obtenemos el trozo de mensaje
    message_slice = mssg[bytes_sent: max_byte]

    # se envía parte del mensaje
    client_socket.sendto(message_slice, server_address)

    # actualizamos cuánto hemos mandado
    bytes_sent += buff_size



