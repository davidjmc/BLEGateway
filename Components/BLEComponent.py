from Amot import Amot

from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle

global our_mac_devices
global our_devices

global our_mac_devices
global our_devices
global peri_nodes

our_mac_devices = ["30:ae:a4:86:a6:06", "9c:9c:1f:e8:e5:a2"]
our_devices = []
peri_nodes = []

#
class ScanDelegate(DefaultDelegate):
    
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handlerDiscovery(self, device, new_device, new_data):
        if new_device:
            print("Discovered device: {0}.".format(device.addr))

        if new_data:
            print("Received new data from: {0}.".format(device.addr))


# 
class MyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__()
        
    def handleNotification(self, hand, data):
        print("Handling notification...")
        print(self)
        print(hand)
        print(struct.unpacl("b", data))


class BLEComponent:

    #
    def __init__(self):
        super().__init__()

        # scans all devices
        self.scannerDevices()
        
        # connecs our devices
        self.connectDevice()
    
    #
    def run(self):

        print("Inside the BLE Component")

        try:
            print("Amount of devices = {}".format(str(len(our_devices))))
            for device in our_devices:
                print("Device {0} ({1}), RSSI={2} dB".format(device.addr, device.addrType, device.rssi))
                
                for(adtype, desc, value) in device.getScanData():
                    print(" {0} = {1}".format(desc, value))
        except:
            pass
    
        Amot.attached(self).run()
    
    #    
    def scannerDevices(self):
        while(len(our_devices) != len(our_mac_devices)):
            scanner = Scanner().withDelegate(ScanDelegate())
            devices = scanner.scan(10.0)
            # print(type(new_devices))
            
            for device in devices:
                if device.addr in our_mac_devices:
                    our_devices.append(device)
            print(our_devices)
            
        
    #
    def connectDevice(self):
        for p in range(len(our_devices)):
            peri_nodes[p] = btle.Peripheral(our_devices[p].addr)
            peri_nodes[p].setDelegate()
        print(peri_nodes)
            
