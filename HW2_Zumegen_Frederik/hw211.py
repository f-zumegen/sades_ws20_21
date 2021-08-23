"""
Smart ESI DimmAdapter with Inheritance
"""

## Imports [DO NOT CHANGE]
## =======================
from hw21x.units import *


## Constants [DO NOT CHANGE]
## =======================
CFG_LED_TEMPERATURE_MAX = Kelvin(350)
CFG_BULB_TEMPERATURE_MAX = Kelvin(500)


## Globals [DO NOT CHANGE]
## =======================
# we use this to read or inject values for your code
g_esi = {
    "ledtemp": Kelvin(300),
    "ledduty": Percent(100),
    "ledvolt": Volt(0),
    "bulbtemp": Kelvin(300),
    "bulbduty": Percent(100),
    "bulbvolt": Volt(0),
}


## Classes
## =======================
class DimmLight:

    # do not change function signature
    def switchState(self, isOn: bool):
        """todo: overwrite or implement"""
        raise NotImplementedError

    # do not change function signature
    def setBrightness(self, lvl: Percent):
        """todo: overwrite or implement"""
        raise NotImplementedError

    # you may add own functions here


class DimmAdapter(DimmLight):
    def __init__(self, name):
        self.name = name

    # set the Voltage level [DO NOT CHANGE]
    def setVoltage(self, voltage: Volt):
        g_esi[self.name + "volt"] = max(0, min(230, voltage))
        print("{} set V={}".format(self.name, g_esi[self.name + "volt"]))

    # set the PWM [DO NOT CHANGE]
    def setPWM(self, duty_cycle: Percent):
        g_esi[self.name + "duty"] = max(0, min(100, duty_cycle))

    # get the temperature in Kelvin [DO NOT CHANGE]
    def temperature(self):
        return Kelvin(g_esi[self.name + "temp"])


class LEDLight(DimmAdapter):
    def __init__(self, name):
        self.name = name

    # todo: your code here

    def switchState(self, isOn: bool):
        if isOn == True and self.temperature() <= CFG_LED_TEMPERATURE_MAX:
            self.setVoltage(Volt(5))

        elif isOn == False:
            self.setVoltage(Volt(0))

    def setBrightness(self, lvl: Percent):
        self.setPWM(lvl / 100)


class BulbLight(DimmAdapter):
    def __init__(self, name):
        self.name = name

    # todo: your code here

    def switchState(self, isOn: bool):
        if isOn == True and self.temperature() <= CFG_BULB_TEMPERATURE_MAX:
            self.setVoltage(Volt(230))

        elif isOn == False:
            self.setVoltage(Volt(0))

    def setBrightness(self, lvl: Percent):
        voltage_level = 230 * lvl / 100
        self.setVoltage(Volt(voltage_level))


# how we might test your code (examples)
# you can uncomment these for testing your solution but make sure
# the following lines are commented before submitting.
# ----------------------------------------------------------
# ledlight = LEDLight('led')
# ledlight.switchState(True)
# ledlight.setBrightness(50)

# bulblight = BulbLight('bulb')
# bulblight.switchState(True)
# bulblight.setBrightness(50)

# our test code
def checkAttribute(key, val):
    if g_esi[key] != val:
        print("ERR: g_esi[{}] == {} != {}".format(key, g_esi[key], val))


ledlight = LEDLight("led")
print(">S0  ", end="")
ledlight.switchState(False)
g_esi["ledtemp"] = 351.0
print(">S1H ", end="")
ledlight.switchState(True)
checkAttribute("ledduty", 0.0)  # only one of them
checkAttribute("ledvolt", 0.0)  # only one of them
g_esi["ledtemp"] = 350.0
print(">S1  ", end="")
ledlight.switchState(True)
checkAttribute("ledvolt", 5.0)
checkAttribute("ledduty", 100.0)
print(">B5  ", end="")
ledlight.setBrightness(50)
checkAttribute("ledduty", 50)
print(">B0  ", end="")
ledlight.setBrightness(0)
checkAttribute("ledduty", 0)

print("== Bulb ==")
bulblight = BulbLight("bulb")
print(">B5  ", end="")
bulblight.setBrightness(50)
checkAttribute("bulbvolt", 115.0)
g_esi["bulbtemp"] = 500.0
print(">S1B8 ", end="")
bulblight.switchState(True)
bulblight.setBrightness(80)
checkAttribute("bulbvolt", 184.0)
print(">B7 ", end="")
bulblight.setBrightness(70)
checkAttribute("bulbvolt", 161.0)