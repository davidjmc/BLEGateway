from bluepy import btle
from bluepy.btle import AssignedNumbers
import struct, os
from concurrent import futures

SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

global macs_from_devices
macs_from_devices = ["9c:9c:1f:e8:e5:a2"]

global devices_global
global delegate_global

class MyDelegate(btle.DefaultDelegate):


    def __init__(self, handle):
        btle.DefaultDelegate.__init__(self)
        self.handle = handle
        print("Created delegate for handle, {0}".format(handle))

    def handleNotification(self, cHandle, data):
        global devices_global
        global delegate_global
        
        for mac in range(len(macs_from_devices)):
            if delegate_global[mac] == self:
                try:      
                    if(cHandle == self.handle):
                        print("HandleNotification for handle: {0}; Raw data: {1}".format(cHandle, data))
                        try:
                            update_thingSpeak(data)
                        except:
                            pass
                    return
                except:
                    pass
                
def new_peripheral(addr):
    global devices_global
    global delegate_global
    
    while True:
        try:
            for mac in range(len(macs_from_devices)):
                if macs_from_devices[mac] == addr:
                    print("Connecting to {0} at index {1}".format(addr, str(mac)))
                    device = btle.Peripheral(addr)
                    
                    service = device.getServiceByUUID(SERVICE_UUID)
                    print("Service: {0}".format(service))
                    
                    measurement = service.getCharacteristics(CHAR_UUID)[0]
                    print("Measurement {0} {1}".format(measurement, measurement.propertiesToString()))
    
                    device.setDelegate(MyDelegate(measurement.getHandle()))
                    
                    devices_global[mac] = device
                    
                    device_loop(device, mac)
        except:
            print("Failed to connect to {}".format(addr))
            continue
        

def device_loop(device, indx):
    while True:
        try:
            if device.waitForNotifications(1.0):
                print("Waiting for notifications...")
                continue
        except:
            try:
                device.disconnect()
            except:
                pass
            print("Disconnecting device: {0}, index: {1}".format(device.addr, indx))
            reestablish_connection(device, device.addr, indx)


def reestablish_connection(device, addr, indx):
    while True:
        try:
            print("Trying to reconnect with: {0}".format(addr))
            device.connect(addr)
            print("re-connected to {0}, index = {1}".format(addr, str(indx)))
            return
        except:
            continue

ex = futures.ProcessPoolExecutor(max_workers=os.cpu_count())
results = ex.map(new_peripheral, macs_from_devices)