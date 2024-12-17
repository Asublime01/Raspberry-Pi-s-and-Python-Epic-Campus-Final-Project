import spidev 
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


def water(num_water):
    print("Watering!!!!")
    GPIO.output(21, GPIO.HIGH)
    time.sleep(2.5)
    GPIO.output(21, GPIO.LOW)
    num_water += 1
    time.sleep(300)
    return num_water

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0 (CS0)
spi.max_speed_hz = 1350000  # Set SPI speed
GPIO.setup([21, 12, 24], GPIO.OUT)
GPIO.setup(16, GPIO.IN) #Set button pin as input
GPIO.output([21, 24, 12], GPIO.LOW) #Turn pump off
GPIO.output(24, GPIO.HIGH) #Turn green light on

num_water = 0
# Function to read ADC channel
def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])  # Start bit + channel
    data = ((adc[1] & 3) << 8) + adc[2]  # Combine the bits
    return data

# Main loop
try:
    while True:
        # Read soil moisture from channel 0
        moisture_level = read_adc(0)
        print("Soil Moisture Level:", moisture_level)
        
        if moisture_level == 0 or moisture_level <= 50:
            num_water = water(num_water)
            if num_water == 4:
                GPIO.output(24, GPIO.LOW) #Turn Green off
                GPIO.output(12, GPIO.HIGH) #turn Red on

                while True:
                    reset = GPIO.input(16) #Listen for button press
                    if reset == 0:
                        GPIO.output(12, GPIO.LOW) #Turn off red
                        GPIO.output(24, GPIO.HIGH) #turn on green
                        num_water = 0
                        break
                    else:
                        reset = GPIO.input(16)
                        continue
        elif moisture_level > 50:
            continue
        
except KeyboardInterrupt:
    print("Program stopped by user")
    spi.close()
