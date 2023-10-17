import SocketTCP
import socket

address = ("localhost", 8000)

server_socketTCP = SocketTCP.SocketTCP()
server_socketTCP.set_socketUDP(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
server_socketTCP.bind(address)
connection_socketTCP, new_address = server_socketTCP.accept()

# test 1
buff_size = 16
full_message = connection_socketTCP.recv(buff_size)
print("Test 1 received:", full_message)
if full_message == "Mensje de len=16".encode(): print("Test 1: Passed")
else: print("Test 1: Failed")