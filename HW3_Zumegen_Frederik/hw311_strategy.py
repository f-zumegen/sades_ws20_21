from abc import ABC, abstractmethod

class packet:
    def __init__(self, data):
        self.data = data

# Interface class for strategy pattern
class Process(ABC):

    @abstractmethod
    def processing(self, p: packet):
        pass

# Context class with which the client interacts
class PacketHandler():
    def __init__(self, packet: packet, process: Process):
        self.packet = packet
        self._process = process

    # Set a strategy
    def setProcess(self, process: Process):
        self._process = process

    # Do the processing
    def doProcessing(self):
        self._process.processing(self, self.packet)

class processSSH(Process):
    def processing(self, p: packet):
        print("Processing SSH")
        print(p.data)
        # more instructions 

class processTLS(Process):
    def processing(self, p: packet):
        print("Processing TLS")
        print(p.data)
        # more instructions 
            
class processIPSEC(Process):
    def processing(self, p: packet):
        print("Processing IPSEC")
        print(p.data)
        # more instructions 

# New policy/strategy example
class processHTTP(Process):
    def processing(self, p: packet):
        print("Processing HTTP")
        print(p.data)
        # more instructions  

def main():
    p = packet("[here is the packet data]")
    handler = PacketHandler(p, processTLS)
    handler.doProcessing()
    handler.setProcess(processHTTP)
    handler.doProcessing()

main()
