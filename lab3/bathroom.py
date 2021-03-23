from VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the

configuration = {
    "name": "bathroom",
    "sheet": "sheet_smarthouse.png",
    "width": 332,
    "height": 300,
    "leds": [
        {"x": 112, "y": 70, "name": "LED 1", "pin": 21},
        {"x": 71, "y": 141, "name": "LED 2", "pin": 22}
    ],
    "buttons": [
        {"x": 242, "y": 146, "name": "Button 1", "pin": 11},
        {"x": 200, "y": 217, "name": "Button 2", "pin": 12},
    ]
}

circuit = TkCircuit(configuration)

@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    from gpiozero import LED, Button
    import paho.mqtt.client as mqtt

    def button_pressed():
        print("button pressed!")
        mqttc.publish("domekMichal/bathroom/light1/toggle", "20", 0, False)

    def button_pressed1():
        mqttc.publish("domekMichal/bathroom/light2/toggle", "20", 0, False)

    led1 = LED(21)

    led2 = LED(22)

    button = Button(11)
    button.when_pressed = button_pressed

    button1 = Button(12)
    button1.when_pressed = button_pressed1
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        mqttc.subscribe("domekMichal/+/zone2/off")
        mqttc.subscribe("domekMichal/bathroom/light1/toggle")
        mqttc.subscribe("domekMichal/bathroom/light2/toggle")


    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        if str(msg.topic).split("/")[2] == "light1":
            led1.toggle()
        elif str(msg.topic).split("/")[2] == "light2":
            led2.toggle()
        elif str(msg.topic).split("/")[1] == "service":
            mqttc.publish("Light controller with michalC5 id is working properly", "20", 0, False)
        else:
            led1.off()
            led2.off()


    # If you want to use a specific client id, use
    mqttc = mqtt.Client("michalC5")
    mqttc.will_set("domekMichal/service", "Light controller with michalC5 id is not working properly", 0, False)

    # but note that the client id must be unique on the broker. Leaving the client
    # id parameter empty will generate a random id for you.
    # mqttc = mqtt.Client("copernicus-test-client")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect

    mqttc.connect("test.mosquitto.org", 1883, 60)

    mqttc.loop_forever()
