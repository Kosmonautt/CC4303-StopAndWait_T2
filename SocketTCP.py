import random
import socket

buff_size = 48

class SocketTCP:
    def __init__(self):
        self.socketUDP = None
        self.dirDestination = None
        self.dirOrigin = None
        self.nSec = None
        # número de puerto al crear un socket de respuesta para el cliente
        self.new_socket_port = None
        self.timeout = 0
        self.buffSize = None
        # dice si queda por leer del mensaje con un recv
        self.bytes_left_to_read = 0
    
    # setters de los diferentes parámetros
    def set_socketUDP(self, socketUDP):
        self.socketUDP = socketUDP

    def set_dirDestination(self, dirDestination):
        self.dirDestination = dirDestination

    def set_nSec(self, nSec):
        self.nSec = nSec

    def set_timeout(self, timeout):
        # timeout en la clase
        self.timeout = timeout
        # timeout en su socketUDP
        self.socketUDP.settimeout(timeout)

    # envía el mensaje (en bytes) dado a la dirección ya seteada con su número de secuencia
    def send_pure(self, mssg):
        self.socketUDP.sendto(mssg, self.dirDestination)

    # recibe un mensaje escuchando en la dirección dada
    def recv_pure(self, buff_size):
        return self.socketUDP.recvfrom(buff_size)
    
    # función que recibe un mensaje codificado y lo envía por completo a un destinatario, lo envía en pedazos
    # de 16 bytes
    def send(self, message):
        # se consigue el largo del mensaje total codificado
        len_mssg = len(message)

        # dice si se envió el largo con éxtio
        length_sent = False
        # se crea la estructura del mensaje con headers con el largo del mensaje total
        struct_lenght = ["0","0","0",str(self.nSec), str(len_mssg)]
        # se pasa a segmento
        message_length = self.create_segment(struct_lenght)

        # se le dice que espero 5 segundos al socket
        self.set_timeout(5)
        # tamaño del buffer del socketUDP, headers+data
        buff_size_UDP = 48

        while not length_sent:
            # se envía el largo del mensaje total
            self.send_pure(message_length.encode())

            # aquí se almacena la respuesta del receptor
            response = None
            # se espera confirmación del receptor
            try:
                # se consige la respuesta de confirmación
                response = (self.recv_pure(buff_size_UDP))[0]
                # se pasa a estructura (PUEDE QUE FALLE SI HAY MUCHO FLUJO, MENSAJE LLEGA MAL, CORREGIR)
                response = self.parse_segment(response.decode())
                # se revisa que tengo un ACK y que el nSec sea correcto
                bool_ACK = response[1] == "1"
                bool_nsec = int(response[3]) == self.nSec + len((str(len_mssg)).encode())

                # si ambos están correctos, se continua y se actualiza el nSec                
                if (bool_ACK and bool_nsec):
                    length_sent = True
                    self.set_nSec(int(response[3]))

            # si es que falla
            except TimeoutError:
                pass

        # bytes del mensaje enviados
        bytes_sent = 0
        # cuántos bytes envía el socketUDP cada vez
        buff_size = 16

        while bytes_sent < len_mssg:
            # máximo byte hasta el que se va a enviar
            max_byte = min(len_mssg, bytes_sent+buff_size)

            # se obtiene el trozo del mensaje que se enviará
            message_slice = message[bytes_sent: max_byte]

            # número de bytes que enviamos
            len_mssg_slice = len(message_slice)

            # se crea estructura del mensaje (con el mensaje en forma de string)
            mssg_slice_struct = ["0","0","0",str(self.nSec),message_slice.decode()]  
            # se pasa a segmento
            seg_slice = self.create_segment(mssg_slice_struct)
            # se envía el segmento
            self.send_pure(seg_slice.encode())

            # se espera la respuesta del receptor
            try:
                #se consigue la respuesta de confirmación
                response = self.recv_pure(buff_size_UDP)[0]
                # se pasa a estructura (PUEDE QUE FALLE SI HAY MUCHO FLUJO, MENSAJE LLEGA MAL, CORREGIR)
                response = self.parse_segment(response.decode())
                # se revisa que tengo un ACK y que el nSec sea correcto
                bool_ACK = response[1] = "1"
                bool_nsec = int(response[3]) == self.nSec + len_mssg_slice

                # si ambos son correctos, se continua con el mensaje
                if(bool_ACK and bool_nsec):
                    # se actualiza la cantidad de bytes enviados
                    bytes_sent+=len_mssg_slice
                    # se actualiza el número de secuencia
                    self.nSec+= len_mssg_slice
            
            # si es que no llega a tiempo el mensaje
            except TimeoutError:
                pass
    
    # función que recibe un mensaje con un tamaño de buffer dado
    def recv(self,buff_size):
        # aquí se guarda el mensaje que retorna
        ret_val = ""

        # tamaño del buffer del socketUDP, headers+data
        buff_size_UDP = 48
        # se recibe el mensaje con el largo del mensaje total
        len_initial_mssg = (self.recv_pure(buff_size_UDP))[0]
        print(len_initial_mssg)
        # se pasa a estructura
        len_initial_mssg = self.parse_segment(len_initial_mssg.decode())
        # se consigue el número de secuencia y la sección de datos
        initial_mssg_sec = len_initial_mssg[3]
        # se consigue la sección de datos
        initial_mssg_data = len_initial_mssg[4]
        # se consigue el largo del mensaje (en bytes) total
        total_lenght = int(initial_mssg_data)
        # se actualiza el número de secuencia
        self.nSec = int(initial_mssg_sec) + len(initial_mssg_data.encode())
        # si es que el mensaje total es más largo quel buffer
        if (total_lenght > buff_size):
            # se setela cuántos bytes faltan por leer en un futuro llamado de recv
            self.bytes_left_to_read = total_lenght - buff_size

        # se envía el mensaje ACK al emisor
        initial_confrm_struct = ["0","1","0",str(self.nSec)]
        # se pasa a seg
        initial_confrm_seg = self.create_segment(initial_confrm_struct)
        # se envía el mensaje al emisor
        self.send_pure(initial_confrm_seg.encode())

        # cuántos bytes hay que recibir
        bytes_to_recieve = min(total_lenght, buff_size)

        # bytes recibidos
        bytes_recieved = 0
        # ahora se empieza a conseguir el mensaje
        while bytes_recieved < bytes_to_recieve:
            # se espera un segmento
            partial_message = (self.recv_pure(buff_size_UDP))[0]
            # se pasa a estructura
            partial_message = self.parse_segment(partial_message.decode())
            # se consigue el número de secuencia y la sección de datos
            mssg_nSec = partial_message[3]
            # se consigue la data
            mssg_data = partial_message[4]
            
            # se revisa si es segmento duplicado
            if(int(mssg_nSec) < self.nSec):
                # se debe enviar el ACK nuevamente
                # se pasa a seg
                ACK_seg = self.create_segment(["0","1","0",str(self.nSec)])
                # se envía el mensaje al emisor
                self.send_pure(ACK_seg.encode())

            # si no es duplicado
            else:
                # se añade el segmento a el mensaje final
                ret_val+= mssg_data
                # se aumenta el número de bytes recibidos
                bytes_recieved += len(mssg_data.encode())
                # se actualiza el número de secuencia
                self.nSec += len(mssg_data.encode())
                # se debe enviar el ACK
                ACK_seg = self.create_segment(["0","1","0",str(self.nSec)])
                # se envía el mensaje al emisor
                self.send_pure(ACK_seg.encode())

        # se retorna el mensaje final (en bytes)
        return ret_val.encode()





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
        # se le inicia el puerto siguiente a los sockets nuevos
        self.new_socket_port = address[1]+1
    
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
        self.send_pure(seg_SYN)

        # se recibe la respuesta  SYN+ACK del server con el mensaje y la dirección de la response
        message_SYN_ACK, response_adress = self.recv_pure(buff_size)
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
        self.send_pure(seg_ACK)

    # función que espera una petición syn, si el handshake
    # se realiza correctamente retorna un nuevo objeto SocketTCP
    def accept(self):
        # se recibe la petición SYN
        message_SYN, address_SYN = self.recv_pure(buff_size)
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
        response_SocketTCP.bind(('localhost',self.new_socket_port))
        # se aumenta el número del puerto para un futuro socket
        self.new_socket_port += 1

        # se crea el mensaje SYN+ACK
        struct_handshake_SYN_ACK = ["1","1","0",str(response_SocketTCP.nSec)]
        # se pasa a segmento
        seg_SYN_ACK = self.create_segment(struct_handshake_SYN_ACK)
        # se pasa a bytes
        seg_SYN_ACK = seg_SYN_ACK.encode()
        # se envía el mensaje
        response_SocketTCP.send_pure(seg_SYN_ACK)

        # se recibe la petición ACK
        message_ACK, address_ACK = response_SocketTCP.recv_pure(buff_size)
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