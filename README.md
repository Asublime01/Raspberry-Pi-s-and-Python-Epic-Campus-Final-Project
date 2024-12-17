
### Project Summary

Our project is a robot that automatically waters a small house plant. Our robot can do this by sensing the moisture of the soil. If the soil is too dry the plant gets watered.


### Technical Overview

To achieve the desired functionality, the project required a water pump, a soil humidity sensor, a set of buttons, and an analog-to-digital converter microchip. The water pump is responsible for transferring water from a reservoir to the plant. To control the pump programmatically, we connected its wires to a transistor, which acts as an electronic switch that can be toggled on and off by supplying it with a control signal.

To obtain data from the soil humidity sensor, we routed its feedback wire through an analog-to-digital converter (ADC) microchip, as the Raspberry Pi lacks native support for analog input. This conversion allowed the Raspberry Pi to process the sensor's analog signals digitally.

With the soil moisture data and pump control in place, we developed a program to automate watering. The code activates the pump for approximately 2.5 seconds when the soil humidity drops below a predefined threshold. Following each watering cycle, the system enters a 3-minute delay to allow water to properly seep into the soil, ensuring accurate subsequent sensor readings.

## List of Materials

- **Input Components**:  
  - Keystudio Soil Humidity Sensor
  - Touch Sensor Button
  - MCP 3008 Microchip

- **Output Components**:  
   -  Green LED (to signal that everything is OK)
   - Red LED (To signal that water needs to be refilled)
   - 5 volt water pump
- **Other Materials**:  
  - Jumper wires
  - NPN transistor
  - T Cobbler
  - Breadboard
  
- **Software Requirements**: 
	- Time module
	- RPi.GPIO module




### Steps Required to Complete the Project
1. Connect pump to 3.3v and ground to make sure it works
2. Test pump with water
3. Figure out how to turn pump on and off with code
4. Connect soil humidity sensor and make sure it is giving humidity data
5. Figure out how to turn pump on and off using the soil humidity data
6. Test without the plant 
7. Test with the plant
8. Finished product

	  

### Test Cases 
1. **Condition:** Soil moisture is below the threshold.  
	**Expected Result:** The robot activates the water pump and waters the plant for a specific duration or until the desired moisture level is reached.

2. **Condition:** Soil moisture is above the threshold.  
	**Expected Result:** The robot does not activate the water pump.
	
3. **Condition:** Water tank is empty while soil moisture is below the threshold.  
	**Expected Result:** The robot turns on its Red LED signaling that the water needs to be refilled
	
4. **Condition:** Power is lost and restored during watering.  
	**Expected Result:** The robot resumes normal operation, checking the soil moisture before deciding whether to water.

## How to Wire

#### Wiring the Pump
- Place a transistor somewhere on the breadboard and make sure you are facing the flat side
- Connect the black cable from the pump to Ground and the Red cable to the far left prong of the transistor
- Connect the middle prong of the transistor to Pin 21
- Connect the far right prong to ground


### Wiring the ADC and Soil Humidity Sensor

#### ***Photo guide is linked it the repository***

#### **Soil Humidity Sensor**
- Connect the VCC / V prong to 3.3v or 5v on your Raspberry Pi
- Connect the GND prong to Ground on your Raspberry Pi
- Connect the S prong to CH0 on the ADC microchip
#####  **ADC Microchip**

Most ADC chips have the following key pins (consult your ADC picture guide for details):

- **VDD/VCC:** Power supply (3.3V or 5V depending on the ADC).
- **GND:** Ground connection.
- **CHn:** Analog input channels (e.g., CH0, CH1, etc.).
- **DIN (MOSI):** Data input from the microcontroller.
- **DOUT (MISO):** Data output to the microcontroller.
- **CLK:** Clock signal for data transfer.
- **CS (Chip Select):** Enables communication with the ADC.

#### **2. Connect Power and Ground**

- Connect the ADC’s **VDD/VCC** pin to the **3.3V or 5V** pin on the Raspberry Pi.
- Connect the ADC’s **GND** pin to the Raspberry Pi’s **GND** pin.


#### **3. Connect the SPI Pins**

Most ADCs use **SPI communication** to send data to the microcontroller. For example, with an MCP3008:

- Connect the **DOUT (MISO)** pin on the ADC to the Raspberry Pi’s **MISO** pin (GPIO 9/Pin 21).
- Connect the **DIN (MOSI)** pin on the ADC to the Raspberry Pi’s **MOSI** pin (GPIO 10/Pin 19).
- Connect the **CLK** pin on the ADC to the Raspberry Pi’s **SCLK** pin (GPIO 11/Pin 23).
- Connect the **CS** pin on the ADC to the Raspberry Pi’s **CE0** pin (GPIO 8/Pin 24).

## How to Run Your Program

This guide explains how to set up and execute your Python program on the Raspberry Pi.

---

### **1. Install Required Libraries**
Ensure Python 3 and `pip` are installed on your Raspberry Pi. Open a terminal (either directly on your Raspberry Pi or via SSH) and run the following commands to install the necessary libraries:

```bash
# Install required libraries
pip install spidev RPi.GPIO

```


### **2. Install  Enable SPI On The Raspberry Pi**
 Run the following in your terminal:
 ```
 sudo raspi-config
 sudo reboot
```

### **3. Set Up and Run the Code**

1. Open **Visual Studio Code** on your computer or connect to the Raspberry Pi via SSH.
2. Create a new Python file, e.g., `water_plant.py`, and paste the provided code into the file.
3. Save the file.


### **4. Run the Program**

1. Open a terminal and navigate to the directory where your file is saved:
    
    bash
    
    Copy code
    
    `cd /path/to/your/code`
    
2. Run the program using Python 3:
    
    bash
    
    Copy code
    
    `python3 water_plant.py`
    

---

### **5. Stop the Program**

To stop the program, press `Ctrl + C` in the terminal.

---

### **6. Notes**

- The program will print the soil moisture levels in the terminal.
- The system will water the plant automatically when moisture drops below the threshold.
- If the system waters 4 times, the **Red LED** will turn on, and you must refill your water container before pressing the **reset button** to continue.
- The **Green LED** indicates normal operation.






# **Resources**

#### **Final photos and videos are linked in the repository**





