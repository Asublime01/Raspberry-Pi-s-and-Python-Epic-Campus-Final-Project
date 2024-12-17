# Import necessary libraries
import spidev  # Library for SPI communication
import time  # Library for time-related functions
import RPi.GPIO as GPIO  # Library for Raspberry Pi GPIO control

# Set up GPIO warnings and pin numbering mode
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering for GPIO

# Function to activate the water pump and count watering cycles
def water(num_water):
    print("Watering!!!!")  # Print message to indicate watering has started
    GPIO.output(21, GPIO.HIGH)  # Turn on the water pump (pin 21)
    time.sleep(2.5)  # Run the pump for 2.5 seconds
    GPIO.output(21, GPIO.LOW)  # Turn off the water pump
    num_water += 1  # Increment the water counter
    time.sleep(300)  # Wait for 5 minutes (300 seconds) before continuing
    return num_water  # Return the updated water count

# Initialize SPI communication
spi = spidev.SpiDev()  # Create an SPI object
spi.open(0, 0)  # Open SPI bus 0, device 0 (CS0)
spi.max_speed_hz = 1350000  # Set SPI communication speed to 1.35 MHz

# Set up GPIO pins
GPIO.setup([21, 12, 24], GPIO.OUT)  # Set pins 21, 12, and 24 as output
GPIO.setup(16, GPIO.IN)  # Set pin 16 as input for the reset button
GPIO.output([21, 24, 12], GPIO.LOW)  # Turn off water pump and lights
GPIO.output(24, GPIO.HIGH)  # Turn on the green LED (pin 24) to indicate "ready"

# Initialize water count
num_water = 0

# Function to read analog data from the ADC (MCP3008)
def read_adc(channel):
    # Ensure the channel number is valid (0-7)
    if channel < 0 or channel > 7:
        return -1  # Return -1 for invalid channel input
    
    # Perform SPI transaction: Start bit + channel selection
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    
    # Combine the 10-bit result from the MCP3008
    data = ((adc[1] & 3) << 8) + adc[2]
    return data  # Return the ADC result

# Main program loop
try:
    while True:
        # Read soil moisture level from channel 0 of the MCP3008
        moisture_level = read_adc(0)
        print("Soil Moisture Level:", moisture_level)  # Display moisture level
        
        # Check if soil moisture is low (<= 50) or no data is received (0)
        if moisture_level == 0 or moisture_level <= 50:
            num_water = water(num_water)  # Water the plant and update counter
            
            # If the plant has been watered 4 times, switch to "reset" mode
            if num_water == 4:
                GPIO.output(24, GPIO.LOW)  # Turn off green LED
                GPIO.output(12, GPIO.HIGH)  # Turn on red LED (pin 12) to indicate alert
                
                # Wait for a button press to reset the system
                while True:
                    reset = GPIO.input(16)  # Check if the reset button (pin 16) is pressed
                    if reset == 0:  # If button is pressed
                        GPIO.output(12, GPIO.LOW)  # Turn off red LED
                        GPIO.output(24, GPIO.HIGH)  # Turn on green LED
                        num_water = 0  # Reset water counter
                        break  # Exit reset mode
                    else:
                        reset = GPIO.input(16)  # Continue checking for button press
                        continue  # Repeat the loop until button press is detected
        
        # If moisture level is sufficient (> 50), do nothing and continue
        elif moisture_level > 50:
            continue

# Handle program exit when interrupted by the user (Ctrl+C)
except KeyboardInterrupt:
    print("Program stopped by user")  # Inform user of program termination
    spi.close()  # Close the SPI communication
