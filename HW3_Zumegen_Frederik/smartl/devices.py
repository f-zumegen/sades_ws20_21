
import datetime

from smartl.config import *
from smartl.observer import *




class Device:
    def __init__(self, name: str):
        self.name = name


# class Light(Device, Observer, ABC): 

#     def update(self, msg: LightConfig):
#         raise NotImplementedError


class Sensor(Device):
    def readVal(self) -> int:
        raise NotImplementedError


# class LightManager:
#     def __init__(self):
#         self._lights = {}

#     def getLight(self, name):
#         return self._lights[name]

#     def addLight(self, l: Light):
#         self._lights[l.name] = l      

#     def delTrigger(self, name):
#         del self._lights[name]



class AmbientSensor(Sensor):
    def __init__(self, name):
        super().__init__(name)  
        self.lastValue = 100

    def measure(self): 
        # simulate 'getting darker'
        self.lastValue = max(self.lastValue-1, 0)

    def readVal(self):
        self.measure()
        print("{} measured {}".format(self.name, self.lastValue))
        return self.lastValue


class Clock(Sensor):
    def __init__(self, name):
        super().__init__(name)  

    def readVal(self):
        hour_now = datetime.datetime.now().hour
        print("{} measured {}".format(self.name, hour_now))
        return hour_now



class HwSwitch(Sensor):
    def __init__(self, name):
        super().__init__(name)
        self._buttons = [False, False]
        
    def pressButton(self, idx: int):
        self._buttons[idx] = True
        print("{}.button[{}] was pressed.".format(self.name, idx))
        #threading.Timer(1, self._releaseButtons).start()

    def _releaseButtons(self):
        self._buttons = [False, False]
        
    def readVal(self):
        return self._buttons[0] + self._buttons[1]*2



# class SwitchLight(Light):
#     def __init__(self, name):
#         super().__init__(name)
#         self._state = False 

#     def switchOn(self):
#         self._state = True
#         print("{} was switched ON!".format(self.name))

#     def switchOff(self):
#         self._state = False
#         print("{} was switched OFF!".format(self.name))

#     def update(self, msg):
#         for change in msg.changes:
#             if isinstance(change, StateChange):
#                 if change.val:
#                     self.switchOn()
#                 else:
#                     self.switchOff()


# class DimmLight(SwitchLight):
#     def __init__(self, name):
#         super().__init__(name) 
#         self.brightness = 0 

#     def setBrightness(self, lvl: Percent):
#         self.brightness = lvl
#         print("{} was dimmed to {}".format(self.name, self.brightness))


#     def update(self, msg: LightConfig):
#         for change in msg.changes:
#             if isinstance(change, StateChange):
#                 if change.val:
#                     self.switchOn()
#                 else:
#                     self.switchOff()

#             if isinstance(change, BrightnessChange):
#                 self.setBrightness(change.val)

