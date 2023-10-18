def close(self):
    # se crea el mensaje de fin para el receptor
    FIN_struct = ["0","0","1",str(self.nSec)]
    # se pasa a seg
    FIN_seg = self.create_segment(FIN_struct)
    # se pasa a bytes
    FIN_seg = FIN_seg.encode()
    # se envía el mensaje que se quiere terminar la comunicacións
    self.send_pure(FIN_seg)

    # se recibe la respuesta 
    response = self.recv_pure(48)[0]
    # se parsea a estcutura
    response = self.parse_segment(response.decode())
    # se verifican los headers y el nSec
    # ACK
    assert response[1] == "1"
    # FIN
    assert response[2] == "1"
    # nSec
    assert int(response[3]) == self.nSec + 1

    # se actualiza el número de secuencia
    self.nSec += 2
    # se crea el mensaje de ACK para el receptor
    ACK_struct = ["0","1","0",str(self.nSec)]
    # se pasa a seg
    ACK_seg = self.create_segment(ACK_struct)
    # se pasa a bytes
    ACK_seg = ACK_seg.encode()
    # se envía el mensaje que se quiere terminar la comunicacións
    self.send_pure(ACK_seg)

def recv_close(self):
    # se recibe la petición de fin 
    request = self.recv_pure(48)[0]
    # se parsea a estcutura
    request = self.parse_segment(request.decode())
    # se verifican los headers y el nSec
    # ACK
    assert request[1] == "0"
    # FIN
    assert request[2] == "1"
    # nSec
    nSec_request = int(request[3])

    # se crea el mensaje de fin ack para el emisor 
    FIN_ACK_struct = ["0","1","1",str(nSec_request+1)]
    # se pasa a seg
    FIN_ACK_seg = self.create_segment(FIN_ACK_struct)
    # se pasa a bytes
    FIN_ACK_seg = FIN_ACK_seg.encode()
    # se envía el mensaje que se quiere terminar la comunicacións
    self.send_pure(FIN_ACK_seg)

    # se recibe la confirmación de fina de fin 
    confirm = self.recv_pure(48)[0]
    # se parsea a estcutura
    confirm = self.parse_segment(confirm.decode())
    # se verifican los headers y el nSec
    # ACK
    assert confirm[1] == "1"
    # nSec
    assert int(confirm[3]) == nSec_request + 2