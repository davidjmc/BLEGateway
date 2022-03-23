from bluepy import btle
from bluepy.btle import AssignedNumbers

import os

from concurrent import futures

macs_from_devices = ["30:ae:a4:86:a6:06", "9c:9c:1f:e8:e5:a2"]

SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

class MyDelegate(btle.DefaultDelegate):

    def __init__(self, handle):
        btle.DefaultDelegate.__init__(self)
        self.handle = handle
        print("Created delegate for handle, {0}".format(handle))

    def handleNotification(self, cHandle, data):
        try:
            if(cHandle == self.handle):
                print("HandleNotification for handle: {0}; Raw data: {1}".format(cHandle, data))
        except:
            pass
            

def new_node(addr):
    print("Connecting...")
    device = btle.Peripheral(addr)

    try:
    
        print("Device services list: \n")
        for svc in device.services:
            print(str(svc))
    
        service = device.getServiceByUUID(SERVICE_UUID)
        print("Service: {0}".format(service))
    
        for char in service.getCharacteristics():
            print("Service char[ {0} ]: {1}".format(char.getHandle(), char))
        
        measurement = service.getCharacteristics(CHAR_UUID)[0]
        print("Measurement {0} {1}".format(measurement, measurement.propertiesToString()))
        
        device.setDelegate(MyDelegate(measurement.getHandle()))
    
        desc = measurement.getDescriptors(AssignedNumbers.client_characteristic_configuration);
        print("Desc {}".format(desc))

        print("Writing \"notification\" flag to descriptor with handle: {0} {1}".format(desc[0].handle, device.writeCharacteristic(desc[0].handle, b"\x01\x00")))# Notice! Do not use [0] in production. Check is descriptor found first!

        print("Waiting for notifications...")
    
        node_loop(device)
        #while True:
            #if device.waitForNotifications(5.0):
                #continue
            #print("Waiting for notifications...")
    
    finally:
        print("Device: {0} desconnected!".format(device))
        device.disconnect();

def node_loop(device):
    while True:
        try:
            if device.waitForNotifications(20.0):
                print("waiting for notifications...")
                continue
        except:
            try:
                device.disconnect()
            except:
                pass
            print("Disconnecting device: {0}".format(device.addr))
            reestablish_connection(device)

def reestablish_connection(device):
    while True:
        try:
            print("trying to reconnect with {0}".format(device.addr))
            perif.connect(device.addr)
            print("re-connected to {0}".format(device.addr))
            return
        except:
            continue


    
ex = futures.ProcessPoolExecutor(max_workers=os.cpu_count())
results = ex.map(new_node, macs_from_devices)