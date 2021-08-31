import bluetooth
import binascii
from tools.logger import Log

class BluetoothRfcommSocket:
    def __init__(self):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def connect(self, bd_addr, port):
        self.sock.connect((bd_addr, port))

    def connectWithUuid(self, bd_addr, uuid):
        port = -1
        services = bluetooth.find_service(address=bd_addr, uuid=uuid)
        for svc in services:
            if svc['protocol'] == 'RFCOMM':
                port = svc['port']
                break
        if port != -1:
            self.sock.connect((bd_addr, port))
        else:
            Log.error('Cannot find target service UUID')

    def send(self, rawdata):
        self.sock.send(rawdata)

    def sendhex(self, hexdata):
        rawdata = binascii.unhexlify(hexdata)
        self.send(rawdata)

    def recv(self, maxsize=1024):
        rawdata = self.sock.recv(maxsize)
        return rawdata

    def recvhex(self, maxsize=1024):
        data = self.recv(maxsize)
        hexdata = binascii.hexlify(data)
        return hexdata

    def close(self):
        self.sock.close()


class BluetoothL2capSocket:
    def __init__(self):
        self.sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)

    def connect(self, bd_addr, port):
        self.sock.connect((bd_addr, port))

    def connectWithUuid(self, bd_addr, uuid):
        port = -1
        services = bluetooth.find_service(address=bd_addr, uuid=uuid)
        for svc in services:
            if svc['protocol'] == 'L2CAP':
                port = svc['port']
                break
        if port != -1:
            self.sock.connect((bd_addr, port))
        else:
            Log.error('Cannot find target service UUID')

    def send(self, rawdata):
        self.sock.send(rawdata)

    def sendhex(self, hexdata):
        rawdata = binascii.unhexlify(hexdata)
        self.send(rawdata)

    def recv(self, maxsize=1024):
        rawdata = self.sock.recv(maxsize)
        return rawdata

    def recvhex(self, maxsize=1024):
        data = self.recv(maxsize)
        hexdata = binascii.hexlify(data)
        return hexdata
    
    def close(self):
        self.sock.close()