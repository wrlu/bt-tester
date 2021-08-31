import sys
import binascii
from stack.btsocket import BluetoothRfcommSocket
from tools.logger import Log


def start_test(socket):
    print('Connected to Bluetooth Secure')
    data = socket.recv()
    print(data)
    socket.sendhex('41')
    print('Data sent...`')


if __name__ == '__main__':
    Log.setLogLevel(Log.LOG_LEVEL_DEBUG)
    # Pixel 2 XL
    bdaddr = '80:5a:04:15:18:1f'
    # AMAP Bluetooth Secure UUID
    uuid = 'FA87C0D0-2199-1724-12CC-0800200C9A66'
    
    socket = BluetoothRfcommSocket()
    socket.connectWithUuid(bdaddr, uuid)
    start_test(socket)
