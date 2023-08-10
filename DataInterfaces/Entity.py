# Map Object Without Name
class BaseMapObject:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


# Map Object With Name
class BaseNamedMapObject(BaseMapObject):
    def __init__(self, x=0, y=0, uid=""):
        super().__init__(x, y)
        self.uid = uid


# Triggers Action, 1 Trigger consists of 10 Actions
class Action:
    def __init__(self, opID=0, args=None):
        if args is None:
            args = []
        self.opID = opID
        self.args = args


# Most used Action at PB2 Triggers Literally the core of whole game
DO_NOTHING = Action(opID=-1, args=[])
