from bluepy import btle
import struct, os
from concurrent import futures

global macs_from_devices
global delegate_global
global perif_global

macs_from_devices = ["30:ae:a4:86:a6:06", "9c:9c:1f:e8:e5:a2"]

SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

class MyDelegate(btle.DefaultDelegate):

    def __init__(self, handle):
        btle.DefaultDelegate.__init__(self)
        self.handle = handle
        print("Created delegate for handle, {0}".format(handle))

    def handleNotification(self, cHandle, data):
        global macs_from_devices
        global delegate_global
        
        for mac in range(len(macs_from_devices)):
                
            if delegate_global[mac] == self:
                try:
                    print("Entrei")
                    return
                except:                    
                    pass
                return
                try:
                    print("Entrei")
                    return
                except:
                    pass
                return

#data_decoded = struct.unpack("b", data)
 #                   perif_global[mac].writeCharacteristic(cHandle,struct.pack("b", 55))
 #                   print("Address: "+addr_var[mac])
  #                  print(data_decoded)

    
    
def perif_loop(perif,indx):
    while True:
        try:
            if perif.waitForNotifications(1.0):
                print("waiting for notifications...")
                continue
        except:
            try:
                perif.disconnect()
            except:
                pass
            print("disconnecting perif: "+perif.addr+", index: "+str(indx))
            reestablish_connection(perif,perif.addr,indx)

def reestablish_connection(perif,addr,indx):
    while True:
        try:
            print("trying to reconnect with "+addr)
            perif.connect(addr)
            print("re-connected to "+addr+", index = "+str(indx))
            return
        except:
            continue

delegate_global = []
perif_global = []
[delegate_global.append(0) for mac in range(len(macs_from_devices))]
[perif_global.append(0) for mac in range(len(macs_from_devices))]

def new_node(addr):
    global delegate_global
    global perif_global
    global macs_from_devices

    while True:
        try:
            for mac in range(len(macs_from_devices)):
                if macs_from_devices[mac] == addr:
                    print("Attempting to connect with "+addr+" at index: "+str(mac))
                    node = btle.Peripheral(addr)
                    perif_global[mac] = node
                    p_delegate = MyDelegate(addr)
                    delegate_global[mac] = p_delegate
                    p.withDelegate(p_delegate)
                    print("Connected to "+addr+" at index: "+str(mac))                    
                    perif_loop(node, mac)
        except:
            check_output("sudo hciconfig hci0 down",shell=True).decode()
            check_output("sudo hciconfig hci0 up",shell=True).decode()
            print("failed to connect to {0}".format(addr))



ex = futures.ProcessPoolExecutor(max_workers = os.cpu_count())
results = ex.map(new_node, macs_from_devices)