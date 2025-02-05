from machine import Pin, ADC, I2C, PWM
from time import sleep_ms, ticks_ms
from ssd1306 import SSD1306_I2C

# Define pin assignments
sdaPin = 16
sclPin = 17
potPin = 28
ledPin = 15
buzzerPin = 18
buttonPin = 14

# Initialize hardware components
led = Pin(ledPin, Pin.OUT)
buzzer = PWM(buzzerPin)
button = Pin(buttonPin, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, sda=Pin(sdaPin), scl=Pin(sclPin), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
potentiometer = ADC(potPin)

# Define global variables
currentButtonState = 0
buttonOn = False
menuIndex = 0
threshold = 25
lastButtonPress = 0

# Function to remap values
def reMap(x1, y1, x2, y2, value):
    m = (y2 - y1) / (x2 - x1)
    newValue = m * (value - x1) + y1
    return newValue

while True:
    # Check button state
    previousButtonState = currentButtonState
    currentButtonState = button.value()

    # Handle button press
    if previousButtonState == 0 and currentButtonState == 1:
        if ticks_ms() - lastButtonPress > 200:  # Debounce button press
            menuIndex = (menuIndex + 1) % 3
            lastButtonPress = ticks_ms()

    # Display and handle menu items
    oled.fill(0)
    if menuIndex == 0:
        oled.text("Menu 1", 0, 0)
        oled.text("Temperature: 25C", 0, 20)
        buzzer.duty_u16(1000)
        buzzer.freq(1000)
        sleep_ms(100)
        buzzer.duty_u16(0)
    elif menuIndex == 1:
        oled.text("Menu 2", 0, 0)
        oled.text("Humidity: 50%", 0, 20)
        buzzer.duty_u16(1000)
        buzzer.freq(1000)
        sleep_ms(100)
        buzzer.duty_u16(0)
        sleep_ms(200)
        buzzer.duty_u16(1000)
        buzzer.freq(1000)
        sleep_ms(100)
        buzzer.duty_u16(0)
    elif menuIndex == 2:
        threshold = int(reMap(0, 20, 65535, 30, potentiometer.read_u16()))
        oled.text("Menu 3", 0, 0)
        oled.text("Threshold: {}C".format(threshold), 0, 20)
        buzzer.duty_u16(1000)
        buzzer.freq(1000)
        sleep_ms(100)
        buzzer.duty_u16(0)
        sleep_ms(200)
        buzzer.duty_u16(1000)
        buzzer.freq(1000)
        sleep_ms(100)
        buzzer.duty_u16(0)
        sleep_ms(200)
        buzzer.duty_u16(1000)
        buzzer.freq(1000)
        sleep_ms(100)
        buzzer.duty_u16(0)
    else:
        menuIndex = 0

        # Check if temperature exceeds threshold
        if 25 > threshold:
            led.value(not led.value())
            buzzer.duty_u16(2000)
            buzzer.freq(500)
            sleep_ms(100)
            buzzer.duty_u16(0)

    oled.show()
