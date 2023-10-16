import socket
import SocketTCP
import sys

# socket no orientado a conexión
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socketTCP
client_socket_TCP = SocketTCP.SocketTCP()
# se le agrega el socket 
client_socket_TCP.socketUDP = client_socket
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
# se asocia al socketTCP
client_socket_TCP.dirDestination = server_address
# se setea seq
client_socket_TCP.set_nSec(100)

# bytes enviados
bytes_sent = 0

# hanshake
client_socket_TCP.connect(server_address)

# while bytes_sent < len_mssg:
#     # máximo bytes hasta el que se va a enviar
#     max_byte = min(len_mssg, bytes_sent + buff_size)

#     # obtenemos el trozo de mensaje (en bytes)
#     message_slice = mssg[bytes_sent: max_byte]

#     # número de bytes que enviamos
#     len_mssg_bytes = len(message_slice)

#     # se actualiza el número de secuencia
#     client_socket_TCP.set_nSec(client_socket_TCP.nSec + len_mssg_bytes)

#     # se crea estructura del mensaje
#     mssg_struct = ["0","0","0",str(client_socket_TCP.nSec), message_slice.decode()]
#     # se crea el mensaje que envía el socket 
#     mssg_to_send = client_socket_TCP.create_segment(mssg_struct)
#     # se pasa a bytes
#     mssg_to_send = mssg_to_send.encode()
#     # se envía el mensaje
#     client_socket_TCP.send_message(mssg_to_send)
#     # actualizamos cuántos bytes se han mandado
#     bytes_sent += len_mssg_bytes




