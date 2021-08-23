""" Rule Engine Example
Your task is to implement another example, similar to the following.
"""

from hw323_rules import RulesEngine, IntCondition, BoolCondition, IntRel, BoolRel, Rule, Action
from smartl.devices import *
from hw322_factory import *
import http.client




def main():
    g_theHour = 0

    def getHour():
        return g_theHour

    def getHttpStatus():
        return r1.status

    def disable_powersaver(x=None):
        print("Will not switch off after 10 minutes.", end='')


    # RuleEngine
    re = RulesEngine()

    # scenario: assume the lights have a power-save mode that will switch them off after 10min
    # create rule: During office hours, the lights should not be in power-save mode
    isAfter8 = IntCondition(getHour, IntRel.GT, 7)
    isBefore18 = IntCondition(getHour, IntRel.LT, 18)
    isWorkingHour= BoolCondition(isAfter8, BoolRel.AND, isBefore18)
    msg = Action(disable_powersaver, None)
    rOfficeLight = Rule("Disabled Power-Saving", isWorkingHour, msg)

    re.addRule(rOfficeLight)

    # Add DimmLight
    # LightManager
    lm = LightManager()
    dimm_lf = DimmLightFactory(lm)

    # create light
    dimm_lf.createLight("LivingRoomLight")

    # use lights
    lm.getLight("LivingRoomLight").switchOn()



    # Rule: Dimm the light when it is passed 8 pm and netflix.com is avilable
    # Important: smartl.trigger import in hw322_factory must be commented out
    isAfter8pm = IntCondition(getHour, IntRel.GT, 19)
    netflixStatusFound = IntCondition(getHttpStatus, IntRel.EQ, 302)
    isMovieTime = BoolCondition(isAfter8pm, BoolRel.AND, netflixStatusFound)
    msg2 = Action(lm.getLight("LivingRoomLight").setBrightness, 30)
    rLivingRoomLight = Rule("Set Movie Light", isMovieTime, msg2)

    re.addRule(rLivingRoomLight)

    # check if netflix.com is available
    conn = http.client.HTTPSConnection("www.netflix.com")
    conn.request("GET", "/")
    r1 = conn.getresponse()

    for hour in range(0,24):
        g_theHour = hour
        print("\nh = {}: ".format(g_theHour), end='')
        
        re.check()


main()
