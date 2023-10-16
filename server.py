import socket
import SocketTCP

# socket no orientado a conexión
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket TCP
server_socket_TCP = SocketTCP.SocketTCP()
# se le agrega el socket 
server_socket_TCP.socketUDP = server_socket
# tamaño del buffer (16 bytes)
buff_size = 48

# puerto usado para la comunicación
port = 8000
# dirrección del servidor
server_address = ('localhost',port)
# se hace bind al socket sever TCP
server_socket_TCP.bind(server_address)

# handshake
connection_socket_TCP, new_adress = server_socket_TCP.accept()

print(new_adress)
print(connection_socket_TCP)

# while True:
#     # se recibe el segmento y la diección desde donde se mandó
#     recv_message, address = server_socket_TCP.recv_message(buff_size)
#     # se pasa el mensaje a string
#     recv_message = recv_message.decode()
#     # se pasa a estrcutura
#     recv_message_struct = server_socket_TCP.parse_segment(recv_message)

#     # se consiguen las diferentes partes del mensaje
#     SYN = recv_message_struct[0]
#     ACK = recv_message_struct[1]
#     FIN = recv_message_struct[2]
#     SEQ = recv_message_struct[3]
#     data = None

#     if (len(recv_message_struct) > 4):
#         data = recv_message_struct[4]

#     # se imprime solo pa rate de data del segmento
#     print(data,end="",flush=True)

