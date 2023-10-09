class socketTCP:
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

    def set_dirOrigin(self, dirOrigin):
        self.dirOrigin = dirOrigin

    def set_nSec(self, nSec):
        self.nSec = nSec
        