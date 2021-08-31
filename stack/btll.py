from internalblue.adbcore import ADBCore
from tools.logger import Log

class LLSocket:
    MODE_NEXUS_5 = 0x0
    MODE_CYPRESS = 0x1

    def __init__(self, mode=None):
        self.session = None
        if mode is None:
            Log.warn('No mode parameter, keep uninit status.')
        elif mode is LLSocket.MODE_NEXUS_5:
            self.initNexus5()
        elif mode is LLSocket.MODE_CYPRESS:
            self.initCypress()
    
    def init(self, mode):
        if mode is None:
            Log.error('No mode parameter, keep uninit status.')
        elif mode is LLSocket.MODE_NEXUS_5:
            self.initNexus5()
        elif mode is LLSocket.MODE_CYPRESS:
            self.initCypress()

    def initNexus5(self):
        if self.session is not None:
            Log.fatal('LLSocket object has already been initilized, device id = '+self.session.interface+'.')
            return
        self.session = ADBCore()
        dev_list = self.session.device_list()
        for dev_obj in dev_list:
            Log.debug('Current device: '+dev_obj[2])
            if 'Nexus 5' in dev_obj[2]:
                Log.info('Found device: '+dev_obj[2])
                self.session.interface = dev_obj[1]
                break
        
        if self.session.interface is None:
            Log.fatal('No Nexus 5 found.')
            self.deInit()
            return
        Log.debug('Start connect')
        if not self.session.connect():
            Log.fatal('Cannot connect to target Nexus 5.')
            self.deInit()
            return
        Log.debug('Start fuzzlmp')
        if not self.session.fuzzLmp():
            Log.fatal('Run fuzzlmp command failed.')
            self.deInit()
            return
        Log.info('Init device: '+self.session.interface+' success.')
    
    def initCypress(self):
        raise NotImplementedError('Cypress boards support is not implemented now.')

    def isInit(self):
        return self.session is not None

    def deInit(self):
        if not self.isInit():
            Log.warn('No session, ignore deInit.')
        elif self.session.interface is None:
            Log.info('No session interface, deInit but ignore shutdown.')
        else:
            Log.debug('Start shutdown')
            self.session.shutdown()
        self.session = None


class BleLcpSocket(LLSocket):
    def sendLcpPacket(self, payload, conn_idx=0):
        if not self.isInit():
            Log.fatal('No session, ignore sendLcpPacket.')
            return
        Log.debug('Start sendLcpPacket, conn_idx = '+str(conn_idx)+'.')
        self.session.sendLcpPacket(conn_idx=conn_idx, payload=payload)


class BtLmpSocket(LLSocket):
    def sendLmpPacket(self, opcode, payload, conn_handle=0x0C):
        if not self.isInit():
            Log.fatal('No session, ignore sendLmpPacket.')
            return
        Log.debug('Start sendLmpPacket, conn_handle = '+str(conn_handle)+'.')
        self.session.sendLmpPacket(opcode=opcode, payload=payload, conn_handle=conn_handle)
