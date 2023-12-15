

import paho.mqtt.client as mqtt

import asyncio
import bleak

from pycycling.cycling_power_service import CyclingPowerService


async def run(address):
    print("Creating async context manager")
    async with bleak.BleakClient(address) as client:
        def my_measurement_handler(data):
            mqttclient.publish("cycling/power",payload=data.instantaneous_power)
            print(data)

        print("Created")
        await client.is_connected()
        print("Connected")
        trainer = CyclingPowerService(client)
        print("CyclingPowerService Init")
        trainer.set_cycling_power_measurement_handler(my_measurement_handler)
        print("Measurement handler set")
        await trainer.enable_cycling_power_measurement_notifications()
        print("Measurement notifications configured")
        await asyncio.sleep(3000.0)
        await trainer.disable_cycling_power_measurement_notifications()


if __name__ == "__main__":
    import os

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(mqttclient, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(mqttclient, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
    mqttclient = mqtt.Client()
    mqttclient.on_connect = on_connect
    mqttclient.on_message = on_message
    mqttclient.connect("mqtt.joshoberhaus.com", 1883, 60)
    mqttclient.loop_start()
    # import wmi
    # brightness = 80 # percentage [0-100] For changing thee screen 
    # c = wmi.WMI(namespace='wmi')
    # methods = c.WmiMonitorBrightnessMethods()[0]    
    # methods.WmiSetBrightness(brightness, 0)

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    device_address = "FA:05:BF:24:96:CC"
    loop = asyncio.get_event_loop()
    print("Event loop retrieved")
    loop.run_until_complete(run(device_address))

