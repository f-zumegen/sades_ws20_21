""" Smart ESI App
"""

# make sure that these imports work
# All class names should be available without namespaces, e.g "Light" not "devices.Light"
from hw23x.devices import *
from hw23x.trigger import *
from hw23x.lightcollections import *


# example main
def main():
    # TriggerManager
    tm = TriggerManager()

    # create light
    l1 = SwitchLight("KitchenLight")
    l1.switchOn()  # switch light

    # sensor
    sens1 = HwSwitch("KitchenSwitch")

    # configs
    cfgOn = LightConfig("ChangeOn")

    # create triggers
    cond1 = IntCondition(1, Relation.EQUALS)
    t1 = Trigger("KitchenManual", sens1, cond1, cfgOn)
    t1.attach(l1)
    tm.addTrigger(t1)

    tm.check()  # check all triggers


# run your code
main()
