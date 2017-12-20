import copy
import system

class FrozenSystem(object):

    def __init__(self):
        self.bodylist = []
        #self.locallistpos = []


    def deepcopySystem(self,system):
        self.bodylist = copy.deepcopy(system.bodylist)
        #self.locallistpos = copy.deepcopy(system.locallistpos)

    def copySystem(self,system):
        self.bodylist = copy.copy(system.bodylist)
        #self.locallistpos = copy.copy(system.locallistpos)

    def get_FrozenPlanet(self,body_ID):
        for b in self.bodylist:
            if b.bodyID == body_ID:
                return b


