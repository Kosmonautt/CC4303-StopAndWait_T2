import SocketTCP

prueba = SocketTCP.SocketTCP()

SYN_ACK = "1|||1|||0|||8|||"
Datos = "0|||0|||0|||98|||Mensaje de prueba"
ACK = "0|||1|||0|||115|||"

# tests
assert SYN_ACK == prueba.create_segment(prueba.parse_segment(SYN_ACK))
assert Datos == prueba.create_segment(prueba.parse_segment(Datos))
assert ACK == prueba.create_segment(prueba.parse_segment(ACK))


print("correcto")