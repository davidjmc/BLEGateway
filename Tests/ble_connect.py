from bluepy import btle
from bluepy.btle import AssignedNumbers
import os
from concurrent import futures

import paho.mqtt.client as mqtt


channelID = "1668795"
apiKey = "8ZP6GXZYIEY7BJ97"
mqttHost = "mqtt.thingspeak.com"
topic = "channels/" + channelID + "/publish/" + apiKey
port = 1883

#global addr_var
#global delegate_global
#global perif_global

SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

macs_from_devices = ["9c:9c:1f:e8:e5:a2", "30:ae:a4:86:a6:06"]

class MyDelegate(btle.DefaultDelegate):

    def __init__(self, handle):
        btle.DefaultDelegate.__init__(self)
        self.handle = handle
        print("Created delegate for handle, {0}".format(handle))

    def handleNotification(self, cHandle, data):
        try:
            if(cHandle == self.handle):
                print("HandleNotification for handle: {0}; Raw data: {1}".format(cHandle, data))
                try:
                    update_thingSpeak(data)
                except:
                    pass
        except:
            pass
            

def device_loop(addr):
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
    
        while True:
            if device.waitForNotifications(5.0):
                continue
            print("Waiting for notifications...")
    
    finally:
        device.disconnect();
        
## http://www.steves-internet-guide.com/client-connections-python-mqtt/
        
def update_thingSpeak(data):
    
    temp, hum = str(data, 'utf-8').split(",")
    tPayload = "field1=" + temp + "&field2=" + hum
    
    client = mqtt.Client("client")
    client.on_connect = on_connect
    client.connect(mqttHost, port)
    
    # attempt to publish this data to the topic
    try:
        client.on_publish = on_publish
        client.publish(topic, payload=tPayload)
        client.disconnect()
    except:
        print ("There was an error while publishing the data.")
        pass
    return

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected ok!")
    else:
        print("Bad connection returned code = {0}".format(rc))

ex = futures.ProcessPoolExecutor(max_workers=os.cpu_count())
results = ex.map(device_loop, macs_from_devices)