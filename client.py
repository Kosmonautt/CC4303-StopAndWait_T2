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
# se le agrega el "end of message"
mssg += "|"
# se pasa a bytes
mssg = mssg.encode()

# puerto usado para la comunicación
port = 8000
# dirección hacia donde se envía el mensaje
server_address = ('localhost',port)

# se envía el mensaje a la dirreción  específicada
aux.send_full_message(client_socket, mssg, "|", server_address, buff_size)


