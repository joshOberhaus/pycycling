import screen_brightness_control as sbc
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(mqttclient, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    mqttclient.subscribe("cycling/power")

# The callback for when a PUBLISH message is received from the server.
def on_message(mqttclient, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    try:
        power = int(msg.payload.decode("utf-8"))
        brightness = 100
        if power > 110:
            brightness = 100
        else:
            brightness = (5/4)*power - 25
            brightness = min(brightness, 100)
            brightness = max(brightness, 2)
        sbc.set_brightness(brightness)
    except ValueError:
        pass
if __name__ == "__main__":
    import os
    mqttclient = mqtt.Client()
    mqttclient.on_connect = on_connect
    mqttclient.on_message = on_message
    mqttclient.connect("mqtt.joshoberhaus.com", 1883, 60)
    mqttclient.loop_forever()