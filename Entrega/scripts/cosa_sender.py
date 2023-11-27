import SocketTCP

address = ("localhost", 8000)

client_socketTCP = SocketTCP.SocketTCP()
client_socketTCP.connect(address)

# debug
#client_socketTCP.debug = True

# test 1
message = "Mensje de len=16".encode()
client_socketTCP.send(message)

