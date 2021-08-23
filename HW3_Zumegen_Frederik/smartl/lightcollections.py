

from smartl.devices import *
# This imnport is needed for my solution in hw322
from hw322_factory import *



class Group(Observer):
    def __init__(self, name):
        self._lights = {}

    def update(self, msg: LightConfig):
        for name, light in self._lights.items():
            light.update(msg)

    #FIXME: add another updateSingleLight(l, c)?

    def addLight(self, l: Light):
        self._lights[l.name] = l

    def delLight(self, name):
        del self._lights[name]



class Scene(Observer):
    def __init__(self, name):
        super().__init__()
        self._group = Group("sg-"+name)
        self._configs = {}

    def update(self, msg: LightConfig):
        if isinstance(msg.changes[0], StateChange) and msg.changes[0].val == 1:          
            for name, config in self._configs.items():
                self._group._lights[name].update(config)

    def addLightAndConfig(self, l: Light, c: LightConfig):
        self._group.addLight(l)
        self._configs[l.name] = c

    def delLight(self, name):
        self._group.delLight(name)
        del self._configs[name]




class GroupManager:
    def __init__(self):
        self._groups = {}

    def addGroup(self, g: Group ):
        self._groups[g.name] = g       

    def getGroup(self, name):
        if name in self._groups:
            return self._groups[name]

    def delGroup(self, name):
        del self._groups[name]




class SceneManager:
    def __init__(self):
        self._scenes = {}

    def addScene( self, s: Scene ):
        self._scenes[s.name] = s     

    def getScene(self, name):
        if name in self._scenes:
            return self._scenes[name]

    def delScene(self, name):
        del self._scenes[name]



