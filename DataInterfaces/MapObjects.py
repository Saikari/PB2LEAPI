from asyncio import gather
from typing import Union
from xml.etree.ElementTree import Element, tostring

from DataInterfaces.Entity import BaseNamedMapObject, BaseMapObject, Action, DO_NOTHING
from DataInterfaces.MapObjectSpecials import RegionActivation


class Timer(BaseNamedMapObject):
    name_counter = 0  # Static counter for naming timers

    def __init__(self, uid=None, x=0, y=0, enabled=False, target=None, delay=0, maxcalls=0):
        super().__init__(x, y, uid)

        if uid is None:
            uid = f"timer_{Timer.name_counter}"
            Timer.name_counter += 1

        self.enabled = enabled
        self.target = target
        self.delay = delay
        self.maxcalls = maxcalls

    @property
    def to_xml(self) -> str:
        ## Dumps timer.
        callback = "-1"
        if self.target is not None:
            callback = self.target

        return f"<timer uid={self.uid}, x={self.x}, y={self.y}, enabled={self.enabled}, maxcalls={self.maxcalls}, target={callback}, delay={self.delay} />"


class Door(BaseNamedMapObject):
    name_counter = 0  # Static counter for naming doors

    def __init__(self, uid=None, x=0, y=0, w=0, h=0, maxspeed=0, tarx=0, tary=0, vis=False, moving=False,
                 attach=None):
        super().__init__(x, y, uid)

        if uid is None:
            uid = f"door_{Door.name_counter}"
            Door.name_counter += 1

        self.w = w
        self.h = h
        self.maxspeed = maxspeed
        self.tarx = tarx
        self.tary = tary
        self.vis = vis
        self.moving = moving
        self.attach = attach

    @property
    def to_xml(self) -> str:
        ## Dumps movable.
        attachTo = "-1"
        if self.attach is not None:
            attachTo = self.attach

        return f"<door uid={self.uid}, vis={self.vis}, x={self.x}, y={self.y}, w={self.w}, h={self.h}, moving={self.moving}, tarx={self.tarx}, tary={self.tary}, attach={attachTo}, maxspeed={self.maxspeed} />"


class Region(BaseNamedMapObject):
    name_counter = 0  # Static counter for naming regions

    def __init__(self, uid=None, x=0, y=0, w=0, h=0, use_target=None, use_on=RegionActivation.NOTHING, attach=None):
        super().__init__(x, y, uid)

        if uid is None:
            uid = f"region_{Region.name_counter}"
            Region.name_counter += 1

        self.w = w
        self.h = h
        self.use_target = use_target
        self.use_on = use_on
        self.attach = attach

    @property
    def to_xml(self) -> str:
        ## Dumps region.
        attachTo = "-1"
        if self.attach is not None:
            attachTo = self.attach
        useTarget = "-1"
        if self.use_target is not None:
            useTarget = self.use_target

        return f"<region uid={self.uid}, x={self.x}, y={self.y}, w={self.w}, h={self.h}, use_target={useTarget}, use_on={self.use_on}, attach={attachTo} />"


class Box(BaseMapObject):
    def __init__(self, x=0, y=0, w=0, h=0, m=0):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.m = m

    @property
    def to_xml(self) -> str:
        ## Dumps wall.
        return f"<box x={self.x}, y={self.y}, w={self.w}, h={self.h}, m={self.m} />"


class Water(BaseMapObject):
    def __init__(self, x=0, y=0, w=0, h=0, damage=0, friction=False):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.damage = damage
        self.friction = friction

    @property
    def to_xml(self) -> str:
        ## Dumps water.
        return f"<water x={self.x}, y={self.y}, w={self.w}, h={self.h}, damage={self.damage}, friction={self.friction} />"


class Decoration(BaseNamedMapObject):
    name_counter = 0  # Static counter for naming decorations

    def __init__(self, x=0, y=0, uid=None, model="", f=0, u=0, v=0, attach=None,
                 r=0, sx=0, sy=0, addx=None, addy=None, at=None):
        super().__init__(x, y, uid)

        if self.uid is None:
            self.uid = f"decor_{Decoration.name_counter}"
            Decoration.name_counter += 1

        self.model = model
        self.f = f
        self.u = u if addx is None else addx
        self.v = v if addy is None else addy
        self.attach = attach if at is None else at
        self.r = r
        self.sx = sx
        self.sy = sy

    @property
    def to_xml(self) -> str:
        ## Dumps decoration.
        attachTo = "-1"
        if self.attach is not None:
            attachTo = self.attach
        return f"<decor uid={self.uid}, x={self.x}, y={self.y}, u={self.u}, v={self.v}, r={self.r}, sx={self.sx}, sy={self.sy}, f={self.f}, model={self.model}, attach={attachTo} />"


class Vehicle(BaseNamedMapObject):
    LEFT = -1
    RIGHT = 1
    name_counter = 0  # Static counter for naming vehicles

    def __init__(self, uid=None, x=0, y=0, side=None, tox=0, toy=0, hpPercent=0, model=""):
        super().__init__()

        if uid is None:
            uid = f"vehicle_{Vehicle.name_counter}"
            Vehicle.name_counter += 1

        self.uid = uid
        self.x = x
        self.y = y

        if side is None:
            side = Vehicle.RIGHT  # Default side value (modify as needed)
        self.side = side

        self.tox = tox
        self.toy = toy
        self.hpPercent = hpPercent
        self.model = model

    @property
    def to_xml(self) -> str:
        ## Dumps vehicle.
        return f"<vehicle uid={self.uid}, x={self.x}, y={self.y}, tox={self.tox}, toy={self.toy}, side={self.side}, hpp={self.hpPercent} />"


class Character(BaseNamedMapObject):
    LEFT = -1
    RIGHT = 1

    player_name_counter = 0  # Static counter for naming player characters
    actor_name_counter = 0  # Static counter for naming actor characters

    def __init__(self, x=0, y=0, uid=None, isPlayer=False, tox=0, toy=0, hea=0, hmax=0, team=0, side=0, char=0,
                 botaction=0, ondeath=None,
                 incar=None):
        super().__init__(x, y, uid)

        if self.uid is None:
            if isPlayer:
                self.uid = f"player_{Character.player_name_counter}"
                Character.player_name_counter += 1
            else:
                self.uid = f"actor_{Character.actor_name_counter}"
                Character.actor_name_counter += 1

        self.isPlayer = isPlayer
        self.tox = tox
        self.toy = toy
        self.hea = hea
        self.hmax = hmax
        self.team = team
        self.side = side
        self.char = char
        self.botaction = botaction
        self.ondeath = ondeath
        self.incar = incar

    @property
    def to_xml(self):
        ## Dumps character.
        onDeath = "-1"
        if self.ondeath is not None:
            onDeath = self.ondeath
        incar = "-1"
        if self.incar is not None:
            incar = self.incar
        a = f"uid={self.uid}, x={self.x}, y={self.y}, tox={self.tox}, toy={self.toy}, hea={self.hea}, hmax={self.hmax}, team={self.team}, side={self.side}, incar={incar}, botaction={self.botaction}, ondeath={onDeath}, char={self.char}"
        if self.isPlayer:
            a = f"<player {a} />"
        else:
            a = f"<actor {a} />"
        return a


class Song(BaseNamedMapObject):
    song_name_counter = 0  # Static counter for naming songs

    def __init__(self, x=0, y=0, uid=None, url="", volume=0, loop=False, callback=None):
        if uid is None:
            uid = f"song_{Song.song_name_counter}"
            Song.song_name_counter += 1

        super().__init__(x, y, uid)
        self.url = url
        self.volume = volume
        self.loop = loop
        self.callback = callback

    @property
    def to_xml(self) -> str:
        ## Dumps song.
        callback = "-1"
        if self.callback is not None:
            callback = self.callback
        return f"<song uid={self.uid}, x={self.x}, y={self.y}, volume={self.volume}, url={self.url}, loop={self.loop}, callback={callback} />"


class EngineMark(BaseMapObject):
    def __init__(self, x=0, y=0, modifier="", parameter=""):
        super().__init__(x, y)
        self.modifier = modifier
        self.parameter = parameter

    @property
    def to_xml(self) -> str:
        ## Dumps engine mark.
        return f"<inf x={self.x}, y={self.y}, mark={self.modifier}, forteam={self.parameter} />"


class Lamp(BaseNamedMapObject):
    lamp_name_counter = 0  # Static counter for naming lamps

    def __init__(self, x=0, y=0, uid=None, power=0.0, flare=False):
        if uid is None:
            uid = f"lamp_{Lamp.lamp_name_counter}"
            Lamp.lamp_name_counter += 1

        super().__init__(x, y, uid)
        self.power = power
        self.flare = flare

    @property
    def to_xml(self) -> str:
        ## Dumps lamp.
        return f"<lamp uid={self.uid}, x={self.x}, y={self.y}, power={self.power}, flare={self.flare} />"


class Barrel(BaseNamedMapObject):
    barrel_name_counter = 0  # Static counter for naming barrels

    def __init__(self, x=0, y=0, uid=None, model=None, tox=0, toy=0):
        if uid is None:
            uid = f"barrel_{Barrel.barrel_name_counter}"
            Barrel.barrel_name_counter += 1

        super().__init__(x, y, uid)

        if model is None:
            model = "bar_orange"

        self.model = model
        self.tox = tox
        self.toy = toy

    @property
    def to_xml(self) -> str:
        ## Dumps barrel.
        return f"<barrel(uid={self.uid}, x={self.x}, y={self.y}, tox={self.tox}, toy={self.toy}, model={self.model} />"


class Gun(BaseNamedMapObject):
    gun_name_counter = 0  # Static counter for naming guns

    def __init__(self, x=0, y=0, uid=None, model="", command=0, upg=0):
        if uid is None:
            uid = f"gun_{Gun.gun_name_counter}"
            Gun.gun_name_counter += 1

        super().__init__(x, y, uid)
        self.model = model
        self.command = command
        self.upg = upg

    @property
    def to_xml(self) -> str:
        ## Dumps weapon.
        return f"<gun uid={self.uid}, x={self.x}, y={self.y}, model={self.model}, upg={self.upg}, command={self.command}/>"


class Pusher(BaseNamedMapObject):
    pusher_name_counter = 0  # Static counter for naming pushers

    def __init__(self, x=0, y=0, uid=None, w=0, h=0, tox=0, toy=0, stabilityDamage=0, damage=0, attachTo=None):
        if uid is None:
            uid = f"pusher_{Pusher.pusher_name_counter}"
            Pusher.pusher_name_counter += 1

        super().__init__(x, y, uid)
        self.w = w
        self.h = h
        self.tox = tox
        self.toy = toy
        self.stabilityDamage = stabilityDamage
        self.damage = damage
        self.attachTo = attachTo

    @property
    def to_xml(self) -> str:
        ## Dumps pusher.
        attachTo = "-1"
        if self.attachTo is not None:
            attachTo = self.attachTo
        return f"<pushf uid={self.uid}, x={self.x}, y={self.y}, w={self.w}, h={self.h}, tox={self.tox}, toy={self.toy}, stab={self.stabilityDamage}, damage={self.damage}, attach={attachTo}/>"


class Background(BaseMapObject):
    def __init__(self, x=0, y=0, w=0, h=0, texX=0, texY=0, f=0, s=False, c="", m="",
                 attach=None):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.u = texX
        self.v = texY
        self.f = f
        self.s = s
        self.c = c
        self.m = m
        self.attach = attach

    @property
    def to_xml(self) -> str:
        ## Dumps background.
        attachTo = "-1"
        if self.attach is not None:
            attachTo = self.attach.uid
        return f"<bg <x={self.x}, y={self.y}, w={self.w}, h={self.h}, c={self.c}, m={self.m}, u={self.u}, v={self.v}, f={self.f}, a={attachTo}, s={self.s} />"


class Trigger(BaseNamedMapObject):
    def __init__(self, x=0, y=0, uid="", enabled=False, maxcalls=0, actions=None, implicitSplitting=True, **kwargs):
        super().__init__(x, y, uid)
        self.implicitSplitting = implicitSplitting
        self.enabled = enabled
        self.maxcalls = maxcalls
        self.actions = []

        for i in range(1, 11):
            action_type = kwargs.get(f"actions_{i}_type")
            if action_type:
                action_args = []
                for arg_key in [f"actions_{i}_targetA", f"actions_{i}_targetB"]:
                    arg_value = kwargs.get(arg_key, "0")
                    action_args.append(arg_value)
                self.actions.append(Action(opID=action_type, args=action_args))

    def addAction(self, action: Union[Action, int], args: list):
        if isinstance(action, int) and args is not None:
            # Make action with opID and args, then add it to self.actions
            result = Action(opID=action, args=args)
            self.actions.append(result)
        elif isinstance(action, Action):
            # Add the provided action to self.actions
            self.actions.append(action)
        else:
            raise ValueError("Invalid arguments provided for addAction function.")

    def move(self, arg1: Union[Door, Region], arg2: Region):
        if isinstance(arg1, Door) and isinstance(arg2, Region):
            # Move movable 'A' to region 'B'
            self.addAction(0, [arg1, arg2])
        elif isinstance(arg1, Region) and isinstance(arg2, Region):
            # Move region 'A' to region 'B'
            self.addAction(2, [arg1, arg2])
        else:
            raise ValueError("Invalid arguments provided for move function.")

    def changeSpeed(self, mov, value):
        ## Change movable 'A' speed to value 'B'
        self.addAction(1, [mov.uid, str(value)])

    def setVariable(self, pbvar1: str, pbvar2: Union[str, int]):
        if isinstance(pbvar2, str):
            # Set variable 'A' to the value of variable 'B'
            self.addAction(125, [pbvar1, pbvar2])
        else:
            # Set variable 'A' to value 'B'
            self.addAction(100, [pbvar1, pbvar2])

    def add(self, pbvar1: str, pbvar2: Union[str, int]):
        if isinstance(pbvar2, str):
            # Add value of variable 'B' to value of variable 'A'
            self.addAction(104, [pbvar1, pbvar2])
        else:
            # Add value 'B' to value of variable 'A'
            self.addAction(102, [pbvar1, str(pbvar2)])

    def setVariableIfUndefined(self, pbvar, value):
        ## Set variable 'A' to value 'B' if variable 'A' is not defined
        self.addAction(101, [pbvar, value])

    def concatenate(self, pbvar1, pbvar2):
        ## Add string-value of variable 'B' at end of variable 'A'
        self.addAction(152, [pbvar1, pbvar2])

    def randomFloat(self, pbvar1: str, pbvar2: Union[str, float]):
        if isinstance(pbvar2, str):
            # Set variable 'A' to random floating number in range 0..X where X is variable
            self.addAction(327, [pbvar1, pbvar2])
        else:
            # Set variable 'A' to random floating number in range 0..B
            self.addAction(106, [pbvar1, str(pbvar2)])

    def randomInt(self, pbvar1: str, pbvar2: Union[str, int]):
        if isinstance(pbvar2, str):
            # Set variable 'A' to random integer number in range 0..X-1 where X is variable
            self.addAction(328, [pbvar1, pbvar2])
        else:
            # Set variable 'A' to random integer number in range 0..B-1
            self.addAction(107, [pbvar1, str(pbvar2)])

    def sendChatMessage(self, who, *texts):
        ## Show text 'A' in chat with color 'B'
        text = "".join(texts)
        self.addAction(42, [text, who])

    def execute(self, target):
        ## Execute trigger 'A'
        self.addAction(99, [target.uid])

    def activate(self, target):
        ## Activate timer 'A'
        self.addAction(25, [target.uid])

    def deactivate(self, target):
        ## Deactivate timer 'A'
        self.addAction(26, [target.uid])

    def sendRequest(self, url, resp):
        ## Request webpage in variable 'A' and save response to variable 'B'
        self.addAction(169, [url, resp])

    def continueEquals(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Continue execution only if variable 'A' equals to variable 'B'
            self.addAction(112, [var1, var2])
        else:
            # Continue execution only if variable 'A' equals to value 'B'
            self.addAction(116, [var1, var2])

    def continueNotEquals(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Continue execution only if variable 'A' is not equal to variable 'B'
            self.addAction(113, [var1, var2])
        else:
            # Continue execution only if variable 'A' is not equal to value 'B'
            self.addAction(117, [var1, var2])

    def replaceVars(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Replace variables in string-value of variable 'B' with their value and save into variable 'A'
            self.addAction(325, [var1, var2])
        else:
            # Replace variables in string-value 'B' with their value and save into variable 'A'
            B = "".join(str(value) for value in var2)
            self.addAction(326, [var1, B])

    def contains(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Set variable 'A' to 1 if variable 'A' contains string-value 'B', set to 0 in else case
            self.addAction(149, [var1, var2])
        else:
            # Set variable 'A' to 1 if variable 'A' contains string-value of variable 'B', set to 0 in else case
            self.addAction(150, [var1, var2])

    def doNothing(self):
        self.addAction(DO_NOTHING)

    def switchLevel(self, map_id):
        ## Complete mission and switch to level id 'A'
        self.addAction(50, [map_id])

    def getCurrent(self, var1):
        ## Set value of variable 'A' to current player slot
        self.addAction(137, [var1])

    def getInitiator(self, var1):
        ## Set value of variable 'A' to slot of player-initiator
        self.addAction(180, [var1])

    def getKiller(self, var1):
        ## Set value of variable 'A' to slot of player-killer
        self.addAction(181, [var1])

    def getTalker(self, var1):
        ## Set value of variable 'A' to slot of player-talker
        self.addAction(159, [var1])

    def getLogin(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Set value of variable 'A' to login of player slot of variable 'B'
            self.addAction(187, [var1, var2])
        else:
            # Set value of variable 'A' to login of player slot 'B'
            self.addAction(184, [var1, str(var2)])

    def getDisplay(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Set value of variable 'A' to display of player slot of variable 'B'
            self.addAction(188, [var1, var2])
        else:
            # Set value of variable 'A' to display of player slot 'B'
            self.addAction(185, [var1, str(var2)])

    def skipIfNotEquals(self, var1, value):
        ## Skip next trigger action if variable 'A' doesnt equal to value 'B'
        self.addAction(123, [var1, value])

    def registerChatListener(self, listener):
        ## Set trigger 'A' as player chat message receiver
        self.addAction(156, [listener.uid])

    def getMessage(self, var1):
        ## Set string-value of variable 'A' to text being said
        self.addAction(160, [var1])

    def sync(self, var1):
        ## Synchronize value of variable 'A' overriding value
        variableCheck(var1)
        self.addAction(223, [var1])

    def syncDefined(self, var1):
        ## Synchronize value of variable 'A' by defined value
        variableCheck(var1)
        self.addAction(224, [var1])

    def syncMax(self, var1):
        ## Synchronize value of variable 'A' by maximum value
        variableCheck(var1)
        self.addAction(225, [var1])

    def syncMin(self, var1):
        ## Synchronize value of variable 'A' by minimum value
        variableCheck(var1)
        self.addAction(226, [var1])

    def syncLongest(self, var1):
        ## Synchronize value of variable 'A' by longest string value
        variableCheck(var1)
        self.addAction(227, [var1])

    async def generate_trigger(self):
        return await self.to_xml()

    @property
    def to_xml(self) -> str:
        if len(self.actions) < 11:
            element = Element("trigger")
            attribs = {
                "uid": self.uid,
                "x": str(self.x),
                "y": str(self.y),
                "enabled": str(self.enabled),
                "maxcalls": str(self.maxcalls)
            }
            for i in range(10):
                action = DO_NOTHING
                if i < len(self.actions):
                    action = self.actions[i]
                args = action.args
                attribs[f"actions_{i + 1}_type"] = str(action.opID)
                if len(args) > 0:
                    attribs[f"actions_{i + 1}_targetA"] = args[0]
                if len(args) > 1:
                    attribs[f"actions_{i + 1}_targetB"] = args[1]
            element.attrib = attribs
            return tostring(element, encoding="unicode")

        # Handle more actions and splitting triggers
        triggers = []
        actionGroups = chunk(self.actions)
        for group in actionGroups:
            if len(group) == 0:
                continue
            if group[-1].opID == 123:
                raise Exception(
                    f"An 'Skip next trigger' action is at the end of trigger {self.uid}. Please fix this yourself.")
            triggers.append(Trigger(
                uid=self.uid,
                x=self.x,
                y=self.y,
                enabled=self.enabled,
                maxcalls=self.maxcalls,
                actions=group
            ))

        result = ""

        # Use asyncio to concurrently generate trigger content
        # tasks = [trigger.to_xml() for trigger in triggers]
        # results = await gather(*tasks)
        # for trigger_result in results:
        #     result += trigger_result + "\n"

        return result


def chunk(actions):
    return [actions[i:i + 9] for i in range(0, len(actions), 9)] + [actions[(len(actions) % 9):]]


def variableCheck(var1):
    forbidden_chars = ['#', '&', ';', '|', '=']
    if any(char in var1 for char in forbidden_chars):
        print(f"[WARNING]: Variable {var1} contains reserved characters: {' '.join(char for char in forbidden_chars if char in var1)}. You cannot synchronize this variable.")
