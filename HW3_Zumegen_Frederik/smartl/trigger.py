

from smartl.devices import *
from smartl.observer import *


class Relation:
    EQUALS='=='
    SMALLER_THAN='<'
    GREATER_THAN='>'



class IntCondition:
    def __init__(self, threshold : int, rel: Relation):
        self._threshold = threshold
        self._relation = rel

    def isTrue(self, inval: int):
        return eval(str(inval) + self._relation + str(self._threshold))  # I know, I know, that's cheating...
        #FIXME: use if statements




class Trigger(Observable):
    def __init__(self, name, sensor: Sensor, cond: IntCondition, config: LightConfig):
        super().__init__()
        self.name = name
        self._sensor = sensor
        self._cond = cond
        self._config = config
        self._wasTrue = False

    def check(self):
        val = self._sensor.readVal()
        if self._cond.isTrue(val):
            if not self._wasTrue:
                self.notify(self._config)
                self._wasTrue = True
        elif self._wasTrue:
            self._wasTrue = False



class TriggerManager:
    def __init__(self):
        self._triggers = {}

    def addTrigger( self, t: Trigger ):
        self._triggers[t.name] = t       

    def delTrigger(self, name):
        del self._triggers[name]


    def check(self):
        for trigg in self._triggers.values():
            trigg.check()

