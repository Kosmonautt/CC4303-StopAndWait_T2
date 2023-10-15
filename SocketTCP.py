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
        if (struct[4] != None):
            seg += struct[4]
        # se retorna el segmento
        return seg
    
    # asocia el socket UDP y la dirección de destino a la dirección dada
    def bind(self, address):
        # origen en el parámetro adress de la clase
        self.dirOrigin = address
        # se le hace bind al socket UDP
        self.socketUDP.bind(address)
