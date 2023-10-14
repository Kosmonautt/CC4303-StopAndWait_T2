import socket

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

while True:
    recv_message, address = server_socket.recvfrom(buff_size)
    print(recv_message.decode(), end='',flush=True)

