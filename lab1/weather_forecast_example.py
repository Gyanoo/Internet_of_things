from VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the
configuration = {
    "name": "CopernicusNG Weather Forecast",
    "sheet": "sheet_forecast.png",
    "width": 343,
    "height": 267,

    "servos": [
        {"x": 170, "y": 150, "length": 90, "name": "Servo 1", "pin": 17}
    ],
    "buttons": [
        {"x": 295, "y": 200, "name": "Button 1", "pin": 11},
        {"x": 295, "y": 170, "name": "Button 2", "pin": 12},
    ]
}


circuit = TkCircuit(configuration)

@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    from time import sleep
    from gpiozero import AngularServo, Button
    from pyowm import OWM

    APIkey = "4526d487f12ef78b82b7a7d113faea64"
    owm = OWM(APIkey)
    manager = owm.weather_manager()
    global currentPlace
    currentPlace = -1

    weatherToIcon = {
        "Thunderstorm": 3,
        "Drizzle": 3,
        "Rain": 3,
        "Snow": 3,
        "Smoke": 2,
        "Haze": 2,
        "Dust": 2,
        "Sand": 2,
        "Ash": 2,
        "Squall": 3,
        "Tornado": 3,
        "Clear": 0,
        "Clouds": 1,
    }

    positions = [-70, -30, 10, 50]
    places = ["Kraków,PL", "Istanbul,TUR", "STOCKHOLM,SE"]

    servo1 = AngularServo(17, min_angle=-90, max_angle=90)

    servo1.angle = -90

    btn = Button(12)

    def get_position(status):
        weather = weatherToIcon.get(status, 0)
        return positions[weather]

    def get_status(place):
        actWeather = manager.weather_at_place(place)
        status = actWeather.weather.status
        return status

    def update():
        global currentPlace
        currentPlace = (currentPlace + 1) % 3
        place = places[currentPlace]
        print("Checking weather for ", place)
        status = get_status(place)
        position = get_position(status)
        servo1.angle = position

    def button_pressed():
        print("button pressed, checking next place")
        update()

    btn.when_pressed = button_pressed
    update()

    while True:
        sleep(1)
