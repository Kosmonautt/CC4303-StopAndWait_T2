import socket
import aux

# socket no orientado a conexión
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# tamaño del buffer (16 bytes)
buff_size = 16

# puerto usado para la comunicación
port = 8000
# dirrección del servidor
server_address = ('localhost',port)
# se hace bind al server
server_socket.bind(server_address)

message, address = aux.receive_full_mesage(server_socket, buff_size, "|")

print(message.decode())


