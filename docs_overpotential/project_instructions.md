# **USER MANUAL FOR OVERPOTENTIAL MEASUREMENT**

<div align="justify">This document is created as a guide for measuring the overpotential of a rechargeable battery using the overpotential circuit and FAIR-Battery Testing Software.
The overpotential of a battery can be determined by calculating the difference between the EMF voltage and the battery voltage, 
both in charging and discharging.<br >
Measuring the overpotential is directly related to the voltage efficiency of the battery.
<br >
<br >
In this procedure, the measurement of the battery EMF voltage is carried out at current of 0.05C (in charging and discharging mode) for approximately 20 hours each.
Then, at a current of 0.5C, the battery voltage measurement is carried out (in charging and discharging mode) (~2 hours each).
The charging and discharging states are switched automatically, indicated by the current mode position in the 
FAIR-Battery Testing Software.</div>

- Total estimated time for measurement: ~45 hours.<br >
- Find the circuit diagram [here](img/Circuit_Full.jpg).

## **A. INSTRUMENTS**
1. Digilent Analog Discovery 2 (AD2)
2. Resistor Bank Circuit
3. Relay Circuit
4. Rechargeable battery
5. Programmable Power Supply (PPS)
6. Adaptor 5V
7. Banana Cables (Black and Red)<br >

![Instrument](img/Full_Set4.jpg)
<div align="center"><strong>Figure 1. Instruments</strong></div>

## **B. METHOD**
### **1. Setup**
**HARDWARE**
- Make sure all cables are connected according to this configuration.
  * For the relay circuit: (see [Relay Circuit](img/Relay_Circuit.png))
    1. Connect the rainbow cable (pins 1 to 8) to AD2 pins 0 to 7 (top pins) respectively. (see [Relay Pin](img/Relay_Pin.png))
    2. Connect the white cable (pin 9) to the AD2 ground pin. (down arrow symbol)
    3. Connect the black cable (pin 9) to the outside (negative) of the 5V adaptor using alligator clips, and the red cable (pin 10) to the tip (positive) of the 5V adaptor. (see [Adaptor Connection](img/Adaptor_Connection.png))
    4. Connect the red banana cable to the PPS (red). (see [Red Cable](img/Red_Cable_PPS.jpeg))<br >
  After connection, make sure the relay circuit is ON (Green LED - ON).
  * For the resistor bank circuit: 
    1. Connect the power cable of the battery to the positive and ground side of the circuit (blue screw terminal, see [Resistor Bank](img/Resistor_Bank.png)).
    2. Connect the black banana cable to the ground of the PPS (black).
  * For the Analog Discover 2 (AD2): (see [AD2](img/AD2.png))
    1. Connect the AD2 to your PC with a USB cable.
    2. Connect the white cable (V+) to hole 3 (I program) of PPS serial port and the grey (V-) to hole 1 (Ø of ref. prog, mon.). (see [PPS Programming](img/Serial.png))
  * For the programmable power supply (PPS):
    1. For safety, remove the red and black output cables during setup.
    2. Enable manual mode by setting both switches in the back to `M`.
    3. Make sure the PPS voltage and current knobs are in the zero position and turn it on.
    4. Turn the current knob to slightly above zero to enable CV mode.
    5. Turn the voltage knob until it shows 1.6 - 1.7V on the display.
    6. Use the rear switch to set current programming mode (`I`: `P`).
    7. Setup is done. Reconnect the front output cables.

**SOFTWARE**
- Download FAIR-Battery Testing Software in this repository
- Setup Python
  1. Prepare your Python environment using [these instructions](../docs/software%20installation.rst), and [these](https://git.science.uu.nl/UED2021/Experiment_Design_2021/-/blob/master/lectures/homework/labphew_lecture_homework.md).
  2. Also use `pip install ruamel.yaml` in the environment.
  3. Open Anaconda Navigator, activate the environment, and launch PyCharm Community.
- In PyCharm:
  1. Open the FAIR-Battery project folder.
  2. Make sure the environment is activated in PyCharm. Check the bottom right corner of PyCharm window.
  3. Go to File -> Setting -> Tools -> Terminal.
  4. In the Environment Variables field, input `PYTHONPATH=.`. Close and reopen the terminal if necessary.
  5. Open the file `Battery_Testing_Software\examples\101_project\BatteryTest_View.py` from the FAIR-Battery folder.
  6. Run it in the terminal: `python Battery_Testing_Software\examples\101_project\BatteryTest_View.py` or click Run (Shift+F10).
- In the FAIR-Battery Testing Window:
  1. Choose File -> Load Test -> `test_config.yml` directly in the FAIR-Battery folder.
  2. Remove the voltage pin cables from the resistor bank circuit and short the cable by using the jumpers according to [this image](img/Short.png).
  3. Calibrate the Bias Voltage: menu Calibration -> Go.
  4. Reconnect the voltage measuring cables to the resistor bank [±2 and ±1 pins](img/Voltage_Pin.png).
  5. Run the program by pressing the Start button.
  6. Make sure the initial state is Discharging (Mode 0).

### **2. Measurement**
- Press the start button.
- The process of charging and discharging is automatically switched in the following steps:
  1. Start in State Discharging (Mode 0), the voltage will decrease rapidly until 1.0V in high current (~30 minutes).
  2. Switch State to Discharging (Mode 1) in low current (~30 minutes). (Due to a bug this may be skipped)
  3. Switch State to Charging (Mode 2) for EMF charge voltage measurement until 1.5V (~20 hours).
  4. Switch State to Discharging (Mode 3) for EMF discharge voltage measurement until 1.0V (~20 hours).
  5. Switch State to Charging (Mode 4) for charge battery voltage measurement until 1.5V (~2 hours).
  6. Switch State to Discharging (Mode 5) for discharge battery voltage measurement until 1.0V (~2 hours).
  7. Switch State to End (Mode 6) where charging and discharging is disabled, data collection continues (indefinitely).
- Press the stop button.
- Save the data: Go to File -> Export to -> Raw Data.
------
**NOTES**
- In case the measurement needs to be paused:
  1. Press the stop button.
  2. Export your data.
  3. Remember your test mode.
- When you want to continue the measurement:
  1. Run `Battery_Testing_Software\examples\101_project\BatteryTest_View.py`.
  2. Choose File -> Load Test -> `test_config.yml` directly in the FAIR-Battery folder.
  3. Choose your test mode.
  4. Start the measurement -> press the start button.
- The datasets need to be combined before analysis.

## **C. DATA ANALYSIS**
**Graph Plot**
- Download [`data_analysis.py`](data_analysis.py) from subproject folder and open it in PyCharm.
- In `data_analysis.py`, change `input_filepath` (line 6) to point at your data file.
- Run the data analysis script. An image is saved automatically.

**Results**

The results of our measurements can be found in [results.md](results.md).<br >
Reference results using a Li-ion battery can be found on page 97 in [V. Pop](https://doi.org/10.1007/978-1-4020-6945-1_4).

<br >
<br >
<div align="center">
<strong>Good luck with the overpotential measurement</strong><br >
<strong>Overpotential Team</strong>
</div>
