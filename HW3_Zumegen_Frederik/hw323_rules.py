"""
Rules Engine
"""

from typing import Callable, Any   # Typing Py3.x

from smartl.devices import *
#from smartl.trigger import *
#from smartl.lightcollections import *
#from hw322_factory import *

import enum

class ICondition:
    def isTrue(self) -> bool:
        raise NotImplementedError 

# Enum classes
class BoolRel:
    NOT = '!='
    AND = '&&'
    OR = '||'

class IntRel:
    EQ = '=='
    GT = '>'
    LT = '<'

# Concrete Classes
class RulesEngine():
    def __init__(self):
        self._rules = {}

    def addRule(self, r):
        self._rules.update({r.name: r})

    def delRule(self, name):
        del self._rules[name]

    # My interpretation of this method: Iterate through 
    # the existing rules to check if their conditions are met
    def check(self):
        for key in self._rules:
            self._rules[key].check()

class Rule():
    def __init__(self, name, cond: ICondition, act):
        self.name = name
        self._cond = cond
        self._act = act

    def Rule(self, name, cond: ICondition, act):
        self.name = name
        self._cond = cond
        self._act = act

    def check(self) -> bool:
        result = self._cond.isTrue()
        # Some debugging:
        # print(result)
        if result == True:
            self._act.exec()
        return result
        
class Action():
    def __init__(self, method: Callable, param: Any):
        self._method = method
        self._param = param

    def exec(self):
        self._method(self._param)

class IntCondition(ICondition):
    def __init__(self, cbVal: Callable, rel: IntRel, thresh: int):
        self._cbVal = cbVal
        self._rel = rel
        self._thresh = thresh

    def isTrue(self) -> bool:
        if self._rel == '==':
            return self._cbVal() == self._thresh
        elif self._rel == '>':
            return self._cbVal() > self._thresh
        elif self._rel == '<':
            return self._cbVal() < self._thresh

class BoolCondition(ICondition):
    def __init__(self, cond1: ICondition, rel: BoolRel, cond2: ICondition):
        self._cond1 = cond1
        self._rel = rel
        self._cond2 = cond2
    
    def isTrue(self) -> bool:
        if self._rel == '!=':
            result = self._cond1.isTrue() != self._cond2.isTrue()
            return result
        elif self._rel == '&&':
            result = self._cond1.isTrue() and self._cond2.isTrue()
            return result
        elif self._rel == '||':
            result = self._cond1.isTrue() or self._cond2.isTrue
            return result

# example test code (same as in hw324)
def main():
    g_theHour = 0

    def getHour():
        return g_theHour

    def disable_powersaver(x=None):
        print("Will not switch off after 10 minutes.", end='')

    # RuleEngine
    re = RulesEngine()

    # scenario: assume the lights have a power-save mode that will switch them off after 10min
    # create rule: During office hours, the lights should not be in power-save mode
    isAfter8 = IntCondition(getHour, IntRel.GT, 7)
    isBefore18 = IntCondition(getHour, IntRel.LT, 18)
    isWorkingHour= BoolCondition(isAfter8, BoolRel.AND, isBefore18)
    msg = Action(disable_powersaver, None)  # None is an optional parameter for Action.method
    rOfficeLight = Rule("Disabled Power-Saving", isWorkingHour, msg)

    re.addRule(rOfficeLight)

    for hour in range(0,24):
        g_theHour = hour
        print("\nh = {}: ".format(g_theHour), end='')
        re.check()


# main()


