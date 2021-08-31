import bluetooth

class SdpClient:

    def __init__(self, bd_addr):
        self.bd_addr = bd_addr

    def findService(self):
        services = bluetooth.find_service(address=self.bd_addr)
        return services
    

class SdpServer:
    pass