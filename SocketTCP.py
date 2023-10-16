import random
import socket

buff_size = 48

class SocketTCP:
    def __init__(self):
        self.socketUDP = None
        self.dirDestination = None
        self.dirOrigin = None
        self.nSec = None
    
    # setters de los diferentes parámetros
    def set_socketUDP(self, socketUDP):
        self.socketUDP = socketUDP

    def set_dirDestination(self, dirDestination):
        self.dirDestination = dirDestination

    def set_nSec(self, nSec):
        self.nSec = nSec

    # envía el mensaje (en bytes) dado a la dirección ya seteada con su número de secuencia
    def send_message(self, mssg):
        self.socketUDP.sendto(mssg, self.dirDestination)

    # recibe un mensaje escuchando en la dirección dada
    def recv_message(self, buff_size):
        return self.socketUDP.recvfrom(buff_size)

    # pasa segmento TCP a estructura
    @staticmethod
    def parse_segment(seg):
        # se divide el segmento por sus separadores
        seg_split = seg.split("|||")
        # se consigue sus headers
        syn = seg_split[0]
        ack = seg_split[1]
        fin = seg_split[2]
        seq = seg_split[3]
        data = None
        # si hay datos se consiguen
        if (len(seg_split) >= 5):
            data = seg_split[4]
        # se crea la estructura 
        struct = [syn, ack, fin, seq, data]

        return struct

    @staticmethod
    def create_segment(struct):
        # se concatenan los headers
        seg = struct[0]+"|||"+struct[1]+"|||"+struct[2]+"|||"+struct[3]+"|||"
        # si hay datos se concatena al mensaje
        if (len(struct) > 4):
            seg += struct[4]
        # se retorna el segmento
        return seg
    
    # asocia el socket UDP y la dirección de destino a la dirección dada
    def bind(self, address):
        # origen en el parámetro adress de la clase
        self.dirOrigin = address
        # se le hace bind al socket UDP
        self.socketUDP.bind(address)
    
    # función que inicia la conexión de un SocketTCP con otro que se encuentra escuchando en la diección adress
    def connect(self, address):
        # número al azar entre 0 y 100 para el número de secuencia
        self.set_nSec(random.randint(0, 100))
        # se setea la dirección de destino
        self.set_dirDestination(address)
        
        # se crea el mensaje SYN del handshake
        struct_handshake = ["1","0","0",str(self.nSec)]
        # se pasa a segmento
        seg_SYN = self.create_segment(struct_handshake)
        # se pasa a bytes
        seg_SYN = seg_SYN.encode()
        # se envía el mensaje
        self.send_message(seg_SYN)

        # se recibe la respuesta  SYN+ACK del server con el mensaje y la dirección de la response
        message_SYN_ACK, response_adress = self.recv_message(buff_size)
        # se setea la nueva dirección de destino
        self.set_dirDestination(response_adress)
        # se pasa el mensaje a una estructura
        struct_handshake_response = self.parse_segment(message_SYN_ACK.decode())

        # se revisa que los headers sean correctos
        # SYN
        assert struct_handshake_response[0] == "1"
        # ACK 
        assert struct_handshake_response[1] == "1"
        # se revisa que el número de secuencia sea correcto
        assert int(struct_handshake_response[3]) == (self.nSec + 1)
        
        # se actualiza el número de secuencia
        self.nSec += 2

        # se manda el mensaje de confirmación al server
        # se crea el mensaje ACK del handshake
        struct_handshake_ACK = ["0","1","0",str(self.nSec)]
        # se pasa a segmento
        seg_ACK = self.create_segment(struct_handshake_ACK)
        # se pasa a bytes
        seg_ACK = seg_ACK.encode()
        # se envía el mensaje
        self.send_message(seg_ACK)

    # función que espera una petición syn, si el handshake
    # se realiza correctamente retorna un nuevo objeto SocketTCP
    def accept(self):
        # se recibe la petición SYN
        message_SYN, address_SYN = self.recv_message(buff_size)
        # se pasa el mensaje a estructura
        struct_handshake_SYN = self.parse_segment(message_SYN.decode())

        # se revisa que los headers sean correctos
        # SYN
        assert struct_handshake_SYN[0] == "1"
        # ACK
        assert struct_handshake_SYN[1] == "0"
        # se consigue el número de secuencia
        nsec_SYN = int(struct_handshake_SYN[3])

        # se crea el socket que se comunicará con el cliente
        response_SocketTCP = SocketTCP()
        # se le da un socket UDP para que funcione
        response_SocketTCP.set_socketUDP(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        # se le setea el número de secuencia
        response_SocketTCP.set_nSec(nsec_SYN+1)
        # se le da una nueva dirección de destino (la del cliente)
        response_SocketTCP.set_dirDestination(address_SYN)
        # se le hace binding a una dirección distinta a la del server
        response_SocketTCP.bind(('localhost',8001)) # agregarque vaya moviendose el coso con un class method

        # se crea el mensaje SYN+ACK
        struct_handshake_SYN_ACK = ["1","1","0",str(response_SocketTCP.nSec)]
        # se pasa a segmento
        seg_SYN_ACK = self.create_segment(struct_handshake_SYN_ACK)
        # se pasa a bytes
        seg_SYN_ACK = seg_SYN_ACK.encode()
        # se envía el mensaje
        response_SocketTCP.send_message(seg_SYN_ACK)

        # se recibe la petición ACK
        message_ACK, address_ACK = response_SocketTCP.recv_message(buff_size)
        # se pasa el mensaje a estructura
        struct_handshake_ACK = self.parse_segment(message_ACK.decode())

        # se revisa que headers, número de secuencia y address sean correctos
        # SYN
        assert struct_handshake_ACK[0] == "0"
        # ACK
        assert struct_handshake_ACK[1] == "1"
        # se consigue el número de secuencia
        nsec_ACK = int(struct_handshake_ACK[3])
        # se revisa que sea correcto
        assert response_SocketTCP.nSec + 1 == nsec_ACK
        # se le setea el nuevo nsec
        response_SocketTCP.set_nSec(nsec_ACK)
        # se revisa que la dirección recibida se la misma
        assert address_ACK == response_SocketTCP.dirDestination

        # finalmente se retorna el socket y adress 
        return response_SocketTCP, response_SocketTCP.dirOrigin