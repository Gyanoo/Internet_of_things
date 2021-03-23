from VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the

configuration = {
    "name": "CopernicusNG SmartHouse lobby",
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
    ],
    "buzzers": [
        {"x": 277, "y": 9, "name": "Buzzer", "pin": 16, "frequency": 440},
    ]
}

circuit = TkCircuit(configuration)



@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    from gpiozero import LED, Button
    import socket
    import struct

    MCAST_GRP = '236.0.0.0'
    MCAST_PORT = 3456

    sockRcv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sockRcv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockRcv.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sockRcv.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    sockSnd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sockSnd.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    led1 = LED(21)
    led2 = LED(22)

    def button1_pressed():
        cmd = "f1;lobby;lamp;1;switch";
        sockSnd.sendto(cmd.encode('utf-8'), (MCAST_GRP, MCAST_PORT))

    def button2_pressed():
        cmd = "*;*;*;*;off";
        sockSnd.sendto(cmd.encode('utf-8'), (MCAST_GRP, MCAST_PORT))

    def handleCommand(cmd):
        print(cmd)
        if cmd[0] in {'f1', '*'} & cmd[1] in {'lobby', '*'} & cmd[2] in {"lamp", '*'} & cmd[3] in {'1', '*'}:
            if cmd[4] == "off":
                led1.off()
            elif cmd[4] == "on":
                led1.on()
            else:
                led1.switch()

    button1 = Button(11)
    button1.when_pressed = button1_pressed

    button2 = Button(12)
    button2.when_pressed = button2_pressed

    while True:
        command = sockRcv.recv(10240)
        command = command.decode("utf-8")
        print(command.split(';'))
        handleCommand(command.split(';'))

