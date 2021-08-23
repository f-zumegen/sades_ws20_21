ON = True
OFF = False


class Observable:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def trigger(self, msg):
        for observer in self.observers:
            observer.update(msg)


class Observer:
    def update(self, msg):
        raise NotImplementedError


# -------------------------------------------------------


class Device:
    def __init__(self, name):
        self.name = name


class Sensor(Observable, Device):
    def __init__(self, name):
        Device.__init__(self, name)
        Observable.__init__(self)

    def read(self):
        raise NotImplementedError

class Light(Observer, Device):
    def __init__(self, name):
        Device.__init__(self, name)

    def update(self, msg):
        raise NotImplementedError


# -------------Switches--------------------------------


class HwSwitch(Sensor):
    def __init__(self, name):
        Sensor.__init__(self, name + " Hardware Switch")
        self.__button1 = OFF
        self.__button2 = OFF
    
    def on(self):
        print("{} was switched ON!".format(self.name))
        self.__button1 = ON
        self.__button2 = OFF
        self.trigger("ON")

    def off(self):
        print("{} was switched OFF!".format(self.name))
        self.__button1 = OFF
        self.__button2 = ON
        self.trigger("OFF")

    def is_on(self):
        return self.__button1


class SwButton(Sensor):
    def __init__(self, name):
        Sensor.__init__(self, name + " Software Switch")
        self.__button = OFF

    def on(self):
        print("{} was switched ON!".format(self.name))
        self.__button = ON
        self.trigger("ON")

    def off(self):
        print("{} was switched OFF!".format(self.name))
        self.__button = OFF
        self.trigger("OFF")

    def is_on(self):
        return self.__button


# ---------------Lights-----------------------------


class SwitchLight(Light):
    def __init__(self, name):
        Light.__init__(self, name)
        self._state = OFF

    def switchOn(self):
        print("{} was switched ON!".format(self.name))
        self._state = ON

    def switchOff(self):
        print("{} was switched OFF!".format(self.name))
        self._state = OFF

    def update(self, msg):
        raise NotImplementedError


class DimmLight(SwitchLight):
    def __init__(self, name):
        SwitchLight.__init__(self, name + " Dimm Light")

    def update(self, msg):
        if msg == "ON":
            self.switchOn()
        if msg == "OFF":
            self.switchOff()

    # def setBrightness(self, lvl):


class BadLight(SwitchLight):
    def __init__(self, name):
        SwitchLight.__init__(self, name + " Bad Light")

    def update(self, msg):
        if msg == "ON":
            self.switchOn()
        if msg == "OFF":
            self.switchOff()


# ---------------------------------------------------------


# main routine
def main():

    # create lights
    l1 = BadLight("Hallway")

    # create buttons
    s1 = SwButton("Door")
    s2 = HwSwitch("Stairs")

    # attach observer
    s1.attach(l1)

    while True:
        user_in = input("\nEnter '1' for 'Door Switch' and '2' for 'Stairs Switch: ")
        if int(user_in) == 1:
            if s1.is_on():
                s1.off()
            else:
                s1.on()
        elif int(user_in) == 2:
            user_in = input("\nEnter '1' to switch Hallway Light on and '2' to switch it off: ")
            if int(user_in) == 1:
                s2.on()
            elif int(user_in) == 2:
                s2.off()       



# run
main()
