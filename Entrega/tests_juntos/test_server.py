import SocketTCP

address = ("localhost", 8000)
server_socketTCP = SocketTCP.SocketTCP()
server_socketTCP.bind(address)
connection_socketTCP, new_address = server_socketTCP.accept()

# debug
# connection_socketTCP.debug = True

# test 1
buff_size = 16
full_message = connection_socketTCP.recv(buff_size)
print("Test 1 received:", full_message)
if full_message == "Mensje de len=16".encode(): print("Test 1: Passed")
else: print("Test 1: Failed")

# test 2
buff_size = 19
full_message = connection_socketTCP.recv(buff_size)
print("Test 2 received:", full_message)
if full_message == "Mensaje de largo 19".encode(): print("Test 2: Passed")
else: print("Test 2: Failed")

# test 3
buff_size = 14
message_part_1 = connection_socketTCP.recv(buff_size)
message_part_2 = connection_socketTCP.recv(buff_size)
print("Test 3 received:", message_part_1 + message_part_2)
if (message_part_1 + message_part_2) == "Mensaje de largo 19".encode(): print("Test 3: Passed")
else: print("Test 3: Failed")

# test 4
buff_size = 14
message_part_1 = connection_socketTCP.recv(buff_size)
message_part_2 = connection_socketTCP.recv(buff_size)
message_part_3 = connection_socketTCP.recv(buff_size)
message_part_4 = connection_socketTCP.recv(buff_size)

print("Test 4 received:", message_part_1 + message_part_2 + message_part_3 + message_part_4)
if (message_part_1 + message_part_2 + message_part_3 + message_part_4) == "Un super test bastante largo de más que 19 bytes".encode(): print("Test 4: Passed")
else: print("Test 4: Failed")

connection_socketTCP.recv_close()

print("fin")