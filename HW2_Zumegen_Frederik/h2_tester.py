

from esi.hw211 import *
from hw211 import *

def testLED(l):
    l.setBrightness(30)
    print(g_esi)
    assert(g_esi[l.name+'volt'] == 0)
    l.switchState(True)
    assert(g_esi[l.name+'volt'] == 10)
    assert(g_esi[l.name+'temp'] <= CFG_LED_TEMPERATURE_MAX)
    l.setBrightness(30)
    assert(g_esi[l.name+'duty'] == 30)
    l.switchState(False)
    assert(g_esi[l.name+'volt'] == 0)
    assert(g_esi[l.name+'temp'] <= CFG_LED_TEMPERATURE_MAX)
    g_esi[l.name+'temp'] = 600



l = LEDLight('led')
testLED(l)


