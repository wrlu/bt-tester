from stack.btsdp import SdpClient
from stack.btsocket import BluetoothRfcommSocket
from tools.logger import Log
from stack.btdiscover import bt_discover

def test_sdp(bdaddr):
    sc = SdpClient(bdaddr)
    services = sc.findService()
    for svc in services:
        print(svc)
    
if __name__ == '__main__':
    Log.setLogLevel(Log.LOG_LEVEL_DEBUG)    
    bdaddr = '80:5a:04:15:18:1f'
    test_sdp(bdaddr)
