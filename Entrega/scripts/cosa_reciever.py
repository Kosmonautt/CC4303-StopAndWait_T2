import SocketTCP

address = ("localhost", 8000)
server_socketTCP = SocketTCP.SocketTCP()
server_socketTCP.bind(address)
connection_socketTCP, new_address = server_socketTCP.accept()

# debug
# connection_socketTCP.debug = True

# test 1
buff_size = 10
full_message = connection_socketTCP.recv(buff_size)
print(full_message)
full_message = connection_socketTCP.recv(buff_size)
print(full_message)

