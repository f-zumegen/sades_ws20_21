"""
Smart ESI LED
"""
from smartl.devices import *

# smartl.trigger is commented out for solution of hw324
from smartl.trigger import *

# from smartl.lightcollections import *
from abc import ABC, abstractmethod

# Abstract "Creator" class
class LightFactory(ABC):
    
    @abstractmethod
    def createLight(self, name):
        pass

    def someOperation(self, name):
        light = self.createLight(name)
        print("Light"+light.name+"created\n")

# Concrete Creator 1
class SwitchLightFactory(LightFactory):
    def __init__(self, lm):
        self.light_manager = lm
    
    def createLight(self, name):
        light = SwitchLight(name)
        self.light_manager.addLight(light)
        return light

# Concrete Creator 2
class DimmLightFactory(LightFactory):
    def __init__(self, lm):
        self.light_manager = lm

    def createLight(self, name):
        light = DimmLight(name)
        self.light_manager.addLight(light)
        return light

# Product interface
# Commented out in devices.py
class Light(Device, Observer, ABC): 

    def update(self, msg: LightConfig):
        pass

# Concrete Product 1
# Commented out in devices.py
class SwitchLight(Light):
    def __init__(self, name):
        super().__init__(name)
        self._state = False 

    def switchOn(self):
        self._state = True
        print("{} was switched ON!".format(self.name))

    def switchOff(self):
        self._state = False
        print("{} was switched OFF!".format(self.name))

    def update(self, msg):
        for change in msg.changes:
            if isinstance(change, StateChange):
                if change.val:
                    self.switchOn()
                else:
                    self.switchOff()

# Concrete Product 2
# Commented out in devices.py
class DimmLight(SwitchLight):
    def __init__(self, name):
        super().__init__(name) 
        self.brightness = 0 

    def setBrightness(self, lvl: Percent):
        self.brightness = lvl
        print("{} was dimmed to {}".format(self.name, self.brightness))


    def update(self, msg: LightConfig):
        for change in msg.changes:
            if isinstance(change, StateChange):
                if change.val:
                    self.switchOn()
                else:
                    self.switchOff()

            if isinstance(change, BrightnessChange):
                self.setBrightness(change.val)

# Commented out in devices.py
class LightManager:
    def __init__(self):
        self._lights = {}

    def getLight(self, name):
        return self._lights[name]

    def addLight(self, l: Light):
        self._lights[l.name] = l      

    def delTrigger(self, name):
        del self._lights[name]

# example usage of your code
# def main():

    # # LightManager
    # lm = LightManager()

    # switch_lf = SwitchLightFactory(lm)

    # # create light
    # switch_lf.createLight("KitchenLight")

    # # use lights
    # lm.getLight("KitchenLight").switchOn()


# when submitting, leave it commented (no execution)
# main()


