from typing import Union
from xml.etree.ElementTree import Element, tostring

from DataInterfaces.Entity import NamedMapObjectEntity, NamelessMapObjectEntity, TriggersActionEntity, DO_NOTHING, \
    ImageEntity
from DataInterfaces.MapObjectSpecials import RegionActivationType


class Timer(NamedMapObjectEntity):
    name_counter = 0  # Static counter for naming timers

    def __init__(self, uid=None, x=0, y=0, enabled=False, target=None, delay=0, maxcalls=0):
        super().__init__(x, y, uid)

        if uid is None:
            self.uid = f"timer_{Timer.name_counter}"
            Timer.name_counter += 1
        self.enabled = enabled
        self.target = target
        self.delay = delay
        self.maxcalls = maxcalls

    @property
    def to_xml(self) -> str:
        # Dumps timer.
        callback = "-1"
        if self.target is not None:
            callback = self.target

        return f'<timer uid="{self.uid}" x="{self.x}" y="{self.y}" enabled="{str(self.enabled).lower()}" ' \
               f'maxcalls="{self.maxcalls}" target="{callback}" delay="{self.delay}" />'


class Door(NamedMapObjectEntity):
    name_counter = 0  # Static counter for naming doors

    def __init__(self, uid=None, x=0, y=0, w=0, h=0, maxspeed=0, tarx=0, tary=0, vis=False, moving=False,
                 attach=None):
        super().__init__(x, y, uid)

        if uid is None:
            self.uid = f"door_{Door.name_counter}"
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
        # Dumps movable.
        attach_to = "-1"
        if self.attach is not None:
            attach_to = self.attach

        return f'<door uid="{self.uid}" vis="{str(self.vis).lower()}" x="{self.x}" y="{self.y}" w="{self.w}" h="{self.h}" ' \
               f'moving="{str(self.moving).lower()}" tarx="{self.tarx}" tary="{self.tary}" ' \
               f'attach="{attach_to}" maxspeed="{self.maxspeed}" />'


class Region(NamedMapObjectEntity):
    name_counter = 0  # Static counter for naming regions

    def __init__(self, uid=None, x=0, y=0, w=0, h=0, use_target=None, use_on=RegionActivationType.NOTHING, attach=None):
        super().__init__(x, y, uid)

        if uid is None:
            self.uid = f"region_{Region.name_counter}"
            Region.name_counter += 1

        self.w = w
        self.h = h
        self.use_target = use_target
        self.use_on = use_on
        self.attach = attach

    @property
    def to_xml(self) -> str:
        # Dumps region.
        attach_to = "-1"
        if self.attach is not None:
            attach_to = self.attach
        use_target = "-1"
        if self.use_target is not None:
            use_target = self.use_target

        return f'<region uid="{self.uid}" x="{self.x}" y="{self.y}" w="{self.w}" h="{self.h}" ' \
               f'use_target="{use_target}" use_on="{self.use_on}" attach="{attach_to}" />'


class Box(NamelessMapObjectEntity):
    def __init__(self, x=0, y=0, w=0, h=0, m=0):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.m = m

    @property
    def to_xml(self) -> str:
        # Dumps wall.
        return f'<box x="{self.x}" y="{self.y}" w="{self.w}" h="{self.h}" m="{self.m}" />'


class Water(NamelessMapObjectEntity):
    def __init__(self, x=0, y=0, w=0, h=0, damage=0, friction=False):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.damage = damage
        self.friction = friction

    @property
    def to_xml(self) -> str:
        # Dumps water.
        return f'<water x="{self.x}" y="{self.y}" w="{self.w}" h="{self.h}" ' \
               f'damage="{self.damage}" friction="{str(self.friction).lower()}" />'


class Decor(NamedMapObjectEntity):
    name_counter = 0  # Static counter for naming decorations

    def __init__(self, x=0, y=0, uid=None, model="", f=0, u=0, v=0, attach=None,
                 r=0, sx=0, sy=0, addx=None, addy=None, at=None):
        super().__init__(x, y, uid)

        if self.uid is None:
            self.uid = f"decor_{Decor.name_counter}"
            Decor.name_counter += 1

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
        # Dumps decoration.
        attach_to = "-1"
        if self.attach is not None:
            attach_to = self.attach
        return f'<decor uid="{self.uid}" x="{self.x}" y="{self.y}" u="{self.u}" v="{self.v}" r="{self.r}" ' \
               f'sx="{self.sx}" sy="{self.sy}" f="{self.f}" model="{self.model}" attach="{attach_to}" />'


class Vehicle(NamedMapObjectEntity):
    LEFT = -1
    RIGHT = 1
    name_counter = 0  # Static counter for naming vehicles

    def __init__(self, uid=None, x=0, y=0, side=None, tox=0, toy=0, hpPercent=0, model=""):
        super().__init__(x, y, uid)  # Call parent class constructor

        if uid is None:
            self.uid = f"vehicle_{Vehicle.name_counter}"
            Vehicle.name_counter += 1

        if side is None:
            self.side = Vehicle.RIGHT  # Default side value (modify as needed)
        else:
            self.side = side

        self.tox = tox
        self.toy = toy
        self.hpPercent = hpPercent
        self.model = model

    @property
    def to_xml(self) -> str:
        # Dumps vehicle.
        return f'<vehicle uid="{self.uid}" x="{self.x}" y="{self.y}" tox="{self.tox}" toy="{self.toy}" ' \
               f'side="{self.side}" hpp="{self.hpPercent}" />'


class Enemy(NamedMapObjectEntity):
    LEFT = -1
    RIGHT = 1

    enemy_name_counter = 0  # Static counter for naming actor characters

    def __init__(self, x=0, y=0, uid=None, tox=0, toy=0, hea=0, hmax=0, team=0, side=0, char=0,
                 botaction=0, ondeath=None,
                 incar=None):
        super().__init__(x, y, uid)

        if self.uid is None:
            self.uid = f"enemy_{Enemy.enemy_name_counter}"
            Enemy.enemy_name_counter += 1

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
        # Dumps character.
        on_death = "-1"
        if self.ondeath is not None:
            on_death = self.ondeath
        incar = "-1"
        if self.incar is not None:
            incar = self.incar
        a = f'<enemy uid="{self.uid}" x="{self.x}" y="{self.y}" tox="{self.tox}" toy="{self.toy}" hea="{self.hea}" ' \
            f'hmax="{self.hmax}" team="{self.team}" side="{self.side}" char="{self.char}" ' \
            f'incar="{incar}" botaction="{self.botaction}" ' \
            f'ondeath="{on_death}" />'
        return a


class Player(NamedMapObjectEntity):
    LEFT = -1
    RIGHT = 1

    player_name_counter = 0  # Static counter for naming player characters

    def __init__(self, x=0, y=0, uid=None, tox=0, toy=0, hea=0, hmax=0, team=0, side=0, char=0,
                 botaction=0, ondeath=None,
                 incar=None):
        super().__init__(x, y, uid)

        if self.uid is None:
            self.uid = f"player_{Player.player_name_counter}"
            Player.player_name_counter += 1

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
        # Dumps character.
        on_death = "-1"
        if self.ondeath is not None:
            on_death = self.ondeath
        incar = "-1"
        if self.incar is not None:
            incar = self.incar
        a = f'<player uid="{self.uid}" x="{self.x}" y="{self.y}" tox="{self.tox}" toy="{self.toy}" hea="{self.hea}" ' \
            f'hmax="{self.hmax}" team="{self.team}" side="{self.side}" char="{self.char}" ' \
            f'incar="{incar}" botaction="{self.botaction}" ' \
            f'ondeath="{on_death}" />'
        return a


class Song(NamedMapObjectEntity):
    song_name_counter = 0  # Static counter for naming songs

    def __init__(self, x=0, y=0, uid=None, url="", volume=0, loop=False, callback=None):
        if uid is None:
            self.uid = f"song_{Song.song_name_counter}"
            Song.song_name_counter += 1

        super().__init__(x, y, uid)
        self.url = url
        self.volume = volume
        self.loop = loop
        self.callback = callback

    @property
    def to_xml(self) -> str:
        # Dumps song.
        callback = "-1"
        if self.callback is not None:
            callback = self.callback
        return f'<song uid="{self.uid}" x="{self.x}" y="{self.y}" volume="{self.volume}" ' \
               f'url="{self.url}" loop="{self.loop}" callback="{callback}" />'


class Inf(NamelessMapObjectEntity):
    def __init__(self, x=0, y=0, mark="", forteam=""):
        super().__init__(x, y)
        self.mark = mark
        self.forteam = forteam

    @property
    def to_xml(self) -> str:
        # Dumps engine mark.
        return f'<inf x="{self.x}" y="{self.y}" mark="{self.mark}" forteam="{self.forteam}" />'


class Lamp(NamedMapObjectEntity):
    lamp_name_counter = 0  # Static counter for naming lamps

    def __init__(self, x=0, y=0, uid=None, power=0.0, flare=False):
        super().__init__(x, y, uid)

        if uid is None:
            self.uid = f"lamp_{Lamp.lamp_name_counter}"
            Lamp.lamp_name_counter += 1

        self.power = power
        self.flare = flare

    @property
    def to_xml(self) -> str:
        # Dumps lamp.
        return f'<lamp uid="{self.uid}" x="{self.x}" y="{self.y}" power="{self.power}" flare="{self.flare}" />'


class Barrel(NamedMapObjectEntity):
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
        # Dumps barrel.
        return f'<barrel uid="{self.uid}" x="{self.x}" y="{self.y}" ' \
               f'tox="{self.tox}" toy="{self.toy}" model="{self.model}" />'


class Gun(NamedMapObjectEntity):
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
        # Dumps weapon.
        return f'<gun uid="{self.uid}" x="{self.x}" y="{self.y}" ' \
               f'model="{self.model}" upg="{self.upg}" command="{self.command}"/>'


class Image(ImageEntity):

    def __init__(self, width=0, height=0, id=0):
        super().__init__(width, height, id)

    @property
    def to_xml(self) -> str:
        # Dumps image.
        return f'<image id="{self.id}" width="{self.width}" height="{self.height}" />'


class Pushf(NamedMapObjectEntity):
    pusher_name_counter = 0  # Static counter for naming pushers

    def __init__(self, x=0, y=0, uid=None, w=0, h=0, tox=0, toy=0, stab=0, damage=0, attach=None):
        if uid is None:
            uid = f"pusher_{Pushf.pusher_name_counter}"
            Pushf.pusher_name_counter += 1

        super().__init__(x, y, uid)
        self.w = w
        self.h = h
        self.tox = tox
        self.toy = toy
        self.stab = stab
        self.damage = damage
        self.attach = attach

    @property
    def to_xml(self) -> str:
        # Dumps pusher.
        # attach_to = "-1"
        # if self.attach is not None:
        # attach_to = self.attach
        return f'<pushf uid="{self.uid}" x="{self.x}" y="{self.y}" w="{self.w}" h="{self.h}" tox="{self.tox}" ' \
               f'toy="{self.toy}" stab="{self.stab}" damage="{self.damage}" attach="{self.attach}"/>'


class Bg(NamelessMapObjectEntity):
    def __init__(self, x=0, y=0, w=0, h=0, texX=0, texY=0, f=0, s=False, c="", m="",
                 a=None):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.u = texX
        self.v = texY
        self.f = f
        self.s = s
        self.c = c
        self.m = m
        self.a = a

    @property
    def to_xml(self) -> str:
        # Dumps background.
        attach_to = "-1"
        if self.a is not None:
            attach_to = self.a
        return f'<bg x="{self.x}" y="{self.y}" w="{self.w}" h="{self.h}" c="{self.c}" ' \
               f'm="{self.m}" u="{self.u}" v="{self.v}" f="{self.f}" a="{attach_to}" s="{str(self.s).lower()}" />'


class Trigger(NamedMapObjectEntity):
    def __init__(self, x=0, y=0, uid="", enabled=False, maxcalls=0, actions=None, implicitSplitting=True, **kwargs):
        super().__init__(x, y, uid)
        if actions is None:
            actions = []
        self.implicitSplitting = implicitSplitting
        self.enabled = enabled
        self.maxcalls = maxcalls
        self.actions = actions

        for i in range(1, 11):
            action_type = kwargs.get(f"actions_{i}_type")
            if action_type:
                action_args = []
                for arg_key in [f"actions_{i}_targetA", f"actions_{i}_targetB"]:
                    arg_value = kwargs.get(arg_key, "0")
                    action_args.append(arg_value)
                self.actions.append(TriggersActionEntity(opID=action_type, args=action_args))

    def add_action(self, action: Union[TriggersActionEntity, int], args: list = None):
        if isinstance(action, int) and args is not None:
            # Make action with opID and args, then add it to self.actions
            result = TriggersActionEntity(opID=action, args=args)
            self.actions.append(result)
        elif isinstance(action, TriggersActionEntity):
            # Add the provided action to self.actions
            self.actions.append(action)
        else:
            raise ValueError("Invalid arguments provided for addAction function.")

    def move(self, arg1: Union[Door, Region], arg2: Region):
        if isinstance(arg1, Door) and isinstance(arg2, Region):
            # Move movable 'A' to region 'B'
            self.add_action(0, [arg1, arg2])
        elif isinstance(arg1, Region) and isinstance(arg2, Region):
            # Move region 'A' to region 'B'
            self.add_action(2, [arg1, arg2])
        else:
            raise ValueError("Invalid arguments provided for move function.")

    def change_speed(self, mov, value):
        # Change movable 'A' speed to value 'B'
        self.add_action(1, [mov.uid, str(value)])

    def set_variable(self, pbvar1: str, pbvar2: Union[str, int]):
        if isinstance(pbvar2, str):
            # Set variable 'A' to the value of variable 'B'
            self.add_action(125, [pbvar1, pbvar2])
        else:
            # Set variable 'A' to value 'B'
            self.add_action(100, [pbvar1, pbvar2])

    def add(self, pbvar1: str, pbvar2: Union[str, int]):
        if isinstance(pbvar2, str):
            # Add value of variable 'B' to value of variable 'A'
            self.add_action(104, [pbvar1, pbvar2])
        else:
            # Add value 'B' to value of variable 'A'
            self.add_action(102, [pbvar1, str(pbvar2)])

    def set_variable_if_undefined(self, pbvar, value):
        # Set variable 'A' to value 'B' if variable 'A' is not defined
        self.add_action(101, [pbvar, value])

    def concatenate(self, pbvar1, pbvar2):
        # Add string-value of variable 'B' at end of variable 'A'
        self.add_action(152, [pbvar1, pbvar2])

    def random_float(self, pbvar1: str, pbvar2: Union[str, float]):
        if isinstance(pbvar2, str):
            # Set variable 'A' to random floating number in range 0..X where X is variable
            self.add_action(327, [pbvar1, pbvar2])
        else:
            # Set variable 'A' to random floating number in range 0..B
            self.add_action(106, [pbvar1, str(pbvar2)])

    def random_int(self, pbvar1: str, pbvar2: Union[str, int]):
        if isinstance(pbvar2, str):
            # Set variable 'A' to random integer number in range 0..X-1 where X is variable
            self.add_action(328, [pbvar1, pbvar2])
        else:
            # Set variable 'A' to random integer number in range 0..B-1
            self.add_action(107, [pbvar1, str(pbvar2)])

    def send_chat_message(self, who, *texts):
        # Show text 'A' in chat with color 'B'
        text = "".join(texts)
        self.add_action(42, [text, who])

    def execute(self, target):
        # Execute trigger 'A'
        self.add_action(99, [target.uid])

    def activate(self, target):
        # Activate timer 'A'
        self.add_action(25, [target.uid])

    def deactivate(self, target):
        # Deactivate timer 'A'
        self.add_action(26, [target.uid])

    def send_request(self, url, resp):
        # Request webpage in variable 'A' and save response to variable 'B'
        self.add_action(169, [url, resp])

    def continue_equals(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Continue execution only if variable 'A' equals to variable 'B'
            self.add_action(112, [var1, var2])
        else:
            # Continue execution only if variable 'A' equals to value 'B'
            self.add_action(116, [var1, var2])

    def continue_not_equals(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Continue execution only if variable 'A' is not equal to variable 'B'
            self.add_action(113, [var1, var2])
        else:
            # Continue execution only if variable 'A' is not equal to value 'B'
            self.add_action(117, [var1, var2])

    def replace_vars(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Replace variables in string-value of variable 'B' with their value and save into variable 'A'
            self.add_action(325, [var1, var2])
        else:
            # Replace variables in string-value 'B' with their value and save into variable 'A'
            b = "".join(str(value) for value in [var2])  # Convert var2 into a list before joining
            self.add_action(326, [var1, b])

    def contains(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Set variable 'A' to 1 if variable 'A' contains string-value 'B', set to 0 in else case
            self.add_action(149, [var1, var2])
        else:
            # Set variable 'A' to 1 if variable 'A' contains string-value of variable 'B', set to 0 in else case
            self.add_action(150, [var1, var2])

    def do_nothing(self):
        self.add_action(DO_NOTHING)

    def switch_level(self, map_id):
        # Complete mission and switch to level id 'A'
        self.add_action(50, [map_id])

    def get_current(self, var1):
        # Set value of variable 'A' to current player slot
        self.add_action(137, [var1])

    def get_initiator(self, var1):
        # Set value of variable 'A' to slot of player-initiator
        self.add_action(180, [var1])

    def get_killer(self, var1):
        # Set value of variable 'A' to slot of player-killer
        self.add_action(181, [var1])

    def get_talker(self, var1):
        # Set value of variable 'A' to slot of player-talker
        self.add_action(159, [var1])

    def get_login(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Set value of variable 'A' to login of player slot of variable 'B'
            self.add_action(187, [var1, var2])
        else:
            # Set value of variable 'A' to login of player slot 'B'
            self.add_action(184, [var1, str(var2)])

    def get_display(self, var1: str, var2: Union[str, int]):
        if isinstance(var2, str):
            # Set value of variable 'A' to display of player slot of variable 'B'
            self.add_action(188, [var1, var2])
        else:
            # Set value of variable 'A' to display of player slot 'B'
            self.add_action(185, [var1, str(var2)])

    def skip_if_not_equals(self, var1, value):
        # Skip next trigger action if variable 'A' doesnt equal to value 'B'
        self.add_action(123, [var1, value])

    def register_chat_listener(self, listener):
        # Set trigger 'A' as player chat message receiver
        self.add_action(156, [listener.uid])

    def get_message(self, var1):
        # Set string-value of variable 'A' to text being said
        self.add_action(160, [var1])

    def sync(self, var1):
        # Synchronize value of variable 'A' overriding value
        variable_check(var1)
        self.add_action(223, [var1])

    def sync_defined(self, var1):
        # Synchronize value of variable 'A' by defined value
        variable_check(var1)
        self.add_action(224, [var1])

    def sync_max(self, var1):
        # Synchronize value of variable 'A' by maximum value
        variable_check(var1)
        self.add_action(225, [var1])

    def sync_min(self, var1):
        # Synchronize value of variable 'A' by minimum value
        variable_check(var1)
        self.add_action(226, [var1])

    def sync_longest(self, var1):
        # Synchronize value of variable 'A' by longest string value
        variable_check(var1)
        self.add_action(227, [var1])

    async def generate_trigger(self):
        return self.to_xml

    @property
    def to_xml(self) -> str:
        if len(self.actions) < 11:
            element = Element("trigger")
            attribs = {
                "uid": self.uid,
                "x": str(self.x),
                "y": str(self.y),
                "enabled": str(self.enabled).lower(),
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
        action_groups = chunk(self.actions)
        for group in action_groups:
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

        for trigger in triggers:
            trigger_result = trigger.to_xml
            result += trigger_result + "\n"

        return result


def chunk(actions):
    return [actions[i:i + 9] for i in range(0, len(actions), 9)] + [actions[(len(actions) % 9):]]


def variable_check(var1):
    forbidden_chars = ['#', '&', ';', '|', '=']
    if any(char in var1 for char in forbidden_chars):
        print(
            f"[WARNING]: Variable {var1} contains reserved characters: "
            f"{' '.join(char for char in forbidden_chars if char in var1)}. "
            "You cannot synchronize this variable.")
