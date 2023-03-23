import time
import board
import digitalio
import busio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO

# Set up LED
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Set up MCP3008 ADC
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D8)
mcp = MCP.MCP3008(spi, cs)
light_channel = AnalogIn(mcp, MCP.P0)
sound_channel = AnalogIn(mcp, MCP.P1)

# Set threshold for light and sound sensors
LIGHT_THRESHOLD = 33000
SOUND_THRESHOLD = 40000

while True:
    # Blink LED 5 times with 500ms intervals
    for i in range(5):
        GPIO.output(LED_PIN, True)
        time.sleep(0.5)
        GPIO.output(LED_PIN, False)
        time.sleep(0.5)

        # Read light sensor for 5 seconds with 100ms intervals
    start_time = time.monotonic()
    while time.monotonic() - start_time < 5:
        light_value = light_channel.value
        if light_value < LIGHT_THRESHOLD:
            print("Light: " + str(light_value) + " (dark)")
        else:
            print("Light: " + str(light_value) + " (bright)")
        time.sleep(0.1)

    # Blink LED 4 times with 200ms intervals
    for i in range(4):
        GPIO.output(LED_PIN, True)
        time.sleep(0.2)
        GPIO.output(LED_PIN, False)
        time.sleep(0.2)

    # Read sound sensor for 5 seconds with 100ms intervals
    start_time = time.monotonic()
    while time.monotonic() - start_time < 5:
        sound_value = sound_channel.value
        print("Sound: " + str(sound_value))
        if sound_value > SOUND_THRESHOLD:
            GPIO.output(LED_PIN, True)
            time.sleep(0.1)
            GPIO.output(LED_PIN, False)
        time.sleep(0.1)
