
Hash256 = int
Percent = int



class ConfigChange:
    def __init__(self, val):
        self.val = val
        

class StateChange(ConfigChange):
    def __init__(self, val: bool):
        super().__init__(val)
        
        
class BrightnessChange(ConfigChange):
    def __init__(self, val: Percent):
        super().__init__(val)





class LightConfig:
    def __init__(self, id: Hash256):
        self.id = id
        self.changes = []

    def addChange(self, change: ConfigChange):
        self.changes.append(change)


