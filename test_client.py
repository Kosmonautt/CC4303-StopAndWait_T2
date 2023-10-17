import SocketTCP
import socket

address = ("localhost", 8000)

client_socketTCP = SocketTCP.SocketTCP()
client_socketTCP.set_socketUDP(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
client_socketTCP.connect(address)

# test 1 
message = "Mensje de len=16".encode()
client_socketTCP.send(message)