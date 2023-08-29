from asyncio import gather
from traceback import format_exc
from typing import Union
from xml.etree.ElementTree import fromstring

from DataInterfaces.Entity import TriggersActionEntity
from DataInterfaces.MapObjectSpecials import EngineMarks
from DataInterfaces.MapObjects import Door, Region, Timer, Vehicle, Box, Water, Decor, Song, Lamp, Barrel, Gun, \
    Pushf, Bg, Enemy, Player, Inf, Trigger, Image


class Map:
    def __init__(self):
        self.objects = {
            Player: [],
            Pushf: [],
            Image: [],
            Bg: [],
            Water: [],
            Box: [],
            Door: [],
            Decor: [],
            Gun: [],
            Region: [],
            Trigger: [],
            Timer: [],
            Inf: [],
            Vehicle: [],
            Song: [],
            Lamp: [],
            Barrel: [],
            Enemy: [],
        }

    def new_object(self, obj_type, **kwargs):
        result = obj_type(**kwargs)
        self.objects[obj_type].append(result)

    def new_movable(self, name, x, y, w, h, tarx, tary=0, speed=10, visible=True, moving=False, attach=None):
        self.new_object(Door, name=name, x=x, y=y, w=w, h=h, tarx=tarx, tary=tary, speed=speed, visible=visible,
                        moving=moving, attach=attach)

    def new_region(self, name, x, y, w, h=0, actTrigger=None, actOn=None, attach=None):
        self.new_object(Region, name=name, x=x, y=y, w=w, h=h, actTrigger=actTrigger, actOn=actOn, attach=attach)

    def new_timer(self, name, x, y=0, enabled=True, callback=None, maxCalls=1, delay=30):
        self.new_object(Timer, name=name, x=x, y=y, enabled=enabled, callback=callback, maxCalls=maxCalls, delay=delay)

    def new_vehicle(self, model="veh_jeep", x=0, y=0, tox=0, toy=0, side=1, hpPercent=100):
        self.new_object(Vehicle, model=model, x=x, y=y, tox=tox, toy=toy, side=side, hpPercent=hpPercent)

    def new_box(self, x, y, w, h, material=0):
        self.new_object(Box, x=x, y=y, w=w, h=h, material=material)

    def new_water(self, x, y, w, h, damage=0, friction=True):
        self.new_object(Water, x=x, y=y, w=w, h=h, damage=damage, friction=friction)

    def new_decoration(self, name, x, y, texX, texY, rotation, layer=0, scaleX=1, scaleY=1, model="stone",
                       attach=None):
        self.new_object(Decor, name=name, x=x, y=y, texX=texX, texY=texY, rotation=rotation, layer=layer,
                        scaleX=scaleX, scaleY=scaleY, model=model, attach=attach)

    def new_song(self, name, x, y=0, url="", volume=1, loop=True, onEnd=None):
        self.new_object(Song, name=name, x=x, y=y, url=url, volume=volume, loop=loop, onEnd=onEnd)

    def new_lamp(self, name, x, y=0, power=0.4, hasFlare=True):
        self.new_object(Lamp, name=name, x=x, y=y, power=power, hasFlare=hasFlare)

    def new_barrel(self, name, x, y, tox, toy=0, model="bar_orange"):
        self.new_object(Barrel, name=name, x=x, y=y, tox=tox, toy=toy, model=model)

    def new_weapon(self, name, x, y, level=0, team=-1, model="gun_rifle"):
        self.new_object(Gun, name=name, x=x, y=y, level=level, team=team, model=model)

    def new_pusher(self, name, x, y, tox, toy, stabilityDamage, damage=0, attach=None):
        self.new_object(Pushf, name=name, x=x, y=y, tox=tox, toy=toy, stabilityDamage=stabilityDamage, damage=damage,
                        attach=attach)

    def new_background(self, x, y, texX, texY, layer=0, hexMultiplier="", showShadow=True, attach=None):
        self.new_object(Bg, x=x, y=y, texX=texX, texY=texY, layer=layer, hexMultiplier=hexMultiplier,
                        showShadow=showShadow, attach=attach)

    def new_enemy(self, name, x, y, tox, toy=0, hea=130, hmax=130, team=0, side=1, char=-1, incar=None, botAction=4,
                  onDeath=None):
        self.new_object(Enemy, name=name, x=x, y=y, tox=tox, toy=toy, hea=hea, hmax=hmax, team=team, side=side,
                        char=char, botAction=botAction, onDeath=onDeath, incar=incar)

    def new_player(self, name, x, y, tox, toy=0, hea=130, hmax=130, team=0, side=1, char=-1, incar=None, botAction=4,
                   onDeath=None):
        self.new_object(Player, name=name, x=x, y=y, tox=tox, toy=toy, hea=hea, hmax=hmax, team=team, side=side,
                        char=char, botAction=botAction, onDeath=onDeath, incar=incar)

    def new_engine_mark(self, x, y=0, modifier=EngineMarks.MARINE_WEAPONS, parameter="0"):
        self.new_object(Inf, x=x, y=y, modifier=modifier, parameter=parameter)

    def parse_trigger(self, trigger_elem):
        trigger = Trigger()

        if trigger_elem.get("uid") is None:
            raise ValueError("Trigger name cannot be empty or missing!")
        trigger.uid = str(trigger_elem.get("uid")) or ""

        trigger.x = int(trigger_elem.get("x")) if trigger_elem.get("x") is not None else 0
        trigger.y = int(trigger_elem.get("y")) if trigger_elem.get("y") is not None else 0
        trigger.enabled = trigger_elem.get("enabled") == "true"
        trigger.maxcalls = int(trigger_elem.get("maxcalls")) if trigger_elem.get("maxcalls") is not None else 0

        for action_elem in trigger_elem.iter("action"):
            action = TriggersActionEntity()
            action.opID = int(action_elem.get("opID")) if action_elem.get("opID") is not None else 0
            action.args = action_elem.get("args").split(",") if action_elem.get("args") else ["0", "0"]
            trigger.actions.append(action)

        self.objects[Trigger].append(trigger)

    def parse_timer(self, timer_elem):
        timer = Timer()

        timer_name = timer_elem.get("uid")
        if timer_name is None:
            raise ValueError("Timer name cannot be empty or missing!")
        timer.uid = str(timer_name)

        timer.x = int(timer_elem.get("x")) if timer_elem.get("x") is not None else 0
        timer.y = int(timer_elem.get("y")) if timer_elem.get("y") is not None else 0
        timer.enabled = bool(timer_elem.get("enabled") == "true")
        timer.maxcalls = int(timer_elem.get("maxcalls")) if timer_elem.get("maxcalls") is not None else 0
        timer.target = timer_elem.get("target") or ""
        timer.delay = float(timer_elem.get("delay")) if timer_elem.get("delay") is not None else 0.0

        self.objects[Timer].append(timer)

    def parse_enemy(self, enemy_elem):
        enemy_name = enemy_elem.get("uid")
        if enemy_name is None:
            raise ValueError("Enemy name cannot be empty or missing!")
        enemy = parse_map_object(Enemy,
                                 **fill_character_kwargs(enemy_name, enemy_elem))
        self.objects[Enemy].append(enemy)

    def parse_player(self, player_elem):
        player_name = player_elem.get("uid")
        if player_name is None:
            raise ValueError("Player name cannot be empty or missing!")
        player = parse_map_object(Player,
                                  **fill_character_kwargs(player_name, player_elem))
        self.objects[Player].append(player)

    def parse_door(self, door_elem):
        door = Door()

        door_name = str(door_elem.get("uid"))
        if door_name is None:
            raise ValueError("Door name cannot be empty or missing!")
        door.uid = str(door_name)

        door.w = int(door_elem.get("w")) if door_elem.get("w") is not None else 0
        door.h = int(door_elem.get("h")) if door_elem.get("h") is not None else 0
        door.y = int(door_elem.get("y")) if door_elem.get("y") is not None else 0
        door.x = int(door_elem.get("x")) if door_elem.get("x") is not None else 0
        door.maxspeed = float(door_elem.get("maxspeed")) if door_elem.get("maxspeed") is not None else 0.0
        door.vis = bool(door_elem.get("vis") == "true")
        door.attach = str(door_elem.get("attach")) if door_elem.get("attach") is not None else "-1"

        self.objects[Door].append(door)

    def parse_decoration(self, decoration_elem):
        decoration = Decor()

        decoration_name = decoration_elem.get("uid")
        if decoration_name is None:
            raise ValueError("Decoration name cannot be empty or missing!")
        decoration.uid = str(decoration_name)

        decoration.model = str(decoration_elem.get("model"))

        decoration.x = int(decoration_elem.get("x")) if decoration_elem.get("x") is not None else 0
        decoration.y = int(decoration_elem.get("y")) if decoration_elem.get("y") is not None else 0
        decoration.f = str(decoration_elem.get("f")) or ""

        decoration.r = float(decoration_elem.get("r")) if decoration_elem.get("r") is not None else 0.0
        decoration.sx = float(decoration_elem.get("sx")) if decoration_elem.get("sx") is not None else 0.0
        decoration.sy = float(decoration_elem.get("sy")) if decoration_elem.get("sy") is not None else 0.0
        decoration.u = float(decoration_elem.get("u")) if decoration_elem.get("u") is not None else 0.0
        decoration.v = float(decoration_elem.get("v")) if decoration_elem.get("v") is not None else 0.0

        decoration.attach = str(decoration_elem.get("attach")) if decoration_elem.get("attach") is not None else "-1"

        self.objects[Decor].append(decoration)

    def parse_region(self, region_elem):
        region = Region()

        region_name = region_elem.get("uid")
        if region_name is None:
            raise ValueError("Region name cannot be empty or missing!")
        region.uid = str(region_name)

        region.x = int(region_elem.get("x")) if region_elem.get("x") is not None else 0
        region.y = int(region_elem.get("y")) if region_elem.get("y") is not None else 0
        region.h = int(region_elem.get("h")) if region_elem.get("h") is not None else 0
        region.w = int(region_elem.get("w")) if region_elem.get("w") is not None else 0

        region.use_on = int(region_elem.get("use_on")) if region_elem.get("use_on") is not None else 0
        region.use_target = region_elem.get("use_target") if region_elem.get("use_target") is not None else ""

        region.attach = str(region_elem.get("attach")) if region_elem.get("attach") is not None else "-1"

        self.objects[Region].append(region)

    def parse_song(self, song_elem):
        song = Song()

        song_name = song_elem.get("uid")
        if song_name is None:
            raise ValueError("Song name cannot be empty or missing!")
        song.uid = str(song_name)

        song.x = int(song_elem.get("x")) if song_elem.get("x") is not None else 0
        song.y = int(song_elem.get("y")) if song_elem.get("y") is not None else 0

        song.loop = bool(song_elem.get("loop") == "true")

        song.url = str(song_elem.get("url"))
        song.volume = float(song_elem.get("volume")) if song_elem.get("volume") is not None else 0.0

        song.callback = str(song_elem.get("callback"))

        self.objects[Song].append(song)

    def parse_lamp(self, lamp_elem):
        lamp = Lamp()

        lamp_name = lamp_elem.get("uid")
        if lamp_name is None:
            raise ValueError("Lamp name cannot be empty or missing!")
        lamp.uid = str(lamp_name)

        lamp.x = int(lamp_elem.get("x")) if lamp_elem.get("x") is not None else 0
        lamp.y = int(lamp_elem.get("y")) if lamp_elem.get("y") is not None else 0

        lamp.power = float(lamp_elem.get("power")) if lamp_elem.get("power") is not None else 0.0

        lamp.flare = bool(lamp_elem.get("flare") == "true")

        self.objects[Lamp].append(lamp)

    def parse_barrel(self, barrel_elem):
        barrel = Barrel()

        barrel_name = barrel_elem.get("uid")
        if barrel_name is None:
            raise ValueError("Barrel name cannot be empty or missing!")
        barrel.uid = str(barrel_name)

        barrel.x = int(barrel_elem.get("x")) if barrel_elem.get("x") is not None else 0
        barrel.y = int(barrel_elem.get("y")) if barrel_elem.get("y") is not None else 0
        barrel.tox = float(barrel_elem.get("tox")) if barrel_elem.get("tox") is not None else 0.0
        barrel.toy = float(barrel_elem.get("toy")) if barrel_elem.get("toy") is not None else 0.0

        barrel.model = str(barrel_elem.get("model")) if barrel_elem.get("model") is not None else "bar_orange"

        self.objects[Barrel].append(barrel)

    def parse_gun(self, gun_elem):
        gun = Gun()

        weapon_name = gun_elem.get("uid")
        if weapon_name is None:
            raise ValueError("Gun name cannot be empty or missing!")
        gun.uid = str(weapon_name)

        gun.x = int(gun_elem.get("x")) if gun_elem.get("x") is not None else 0
        gun.y = int(gun_elem.get("y")) if gun_elem.get("y") is not None else 0
        gun.command = int(gun_elem.get("command")) if gun_elem.get("command") is not None else 0
        gun.upg = int(gun_elem.get("upg")) if gun_elem.get("upg") is not None else 0

        gun.model = str(gun_elem.get("model"))

        self.objects[Gun].append(gun)

    def parse_pusher(self, pusher_elem):
        pusher = Pushf()

        pusher_name = pusher_elem.get("uid")
        if pusher_name is None:
            raise ValueError("Pusher name cannot be empty or missing!")
        pusher.uid = str(pusher_name)

        pusher.x = int(pusher_elem.get("x")) if pusher_elem.get("x") is not None else 0
        pusher.y = int(pusher_elem.get("y")) if pusher_elem.get("y") is not None else 0
        pusher.h = int(pusher_elem.get("h")) if pusher_elem.get("h") is not None else 0
        pusher.w = int(pusher_elem.get("w")) if pusher_elem.get("w") is not None else 0
        pusher.tox = float(pusher_elem.get("tox")) if pusher_elem.get("tox") is not None else 0.0
        pusher.toy = float(pusher_elem.get("toy")) if pusher_elem.get("toy") is not None else 0.0
        pusher.attach = str(pusher_elem.get("attach")) if pusher_elem.get("attach") is not None else "-1"
        pusher.damage = float(pusher_elem.get("damage")) if pusher_elem.get("damage") is not None else 0.0
        pusher.stab = float(pusher_elem.get("stab")) if pusher_elem.get("stab") is not None else 0.0

        self.objects[Pushf].append(pusher)

    def parse_vehicle(self, vehicle_elem):
        vehicle = Vehicle()

        vehicle_name = vehicle_elem.get("uid")
        if vehicle_name is None:
            raise ValueError("Vehicle name cannot be empty or missing!")
        vehicle.uid = str(vehicle_name)

        vehicle.x = int(vehicle_elem.get("x")) if vehicle_elem.get("x") is not None else 0
        vehicle.y = int(vehicle_elem.get("y")) if vehicle_elem.get("y") is not None else 0
        vehicle.side = int(vehicle_elem.get("side")) if vehicle_elem.get("side") is not None else 0

        vehicle.model = str(vehicle_elem.get("model")) if vehicle_elem.get("model") is not None else "veh_jeep"

        vehicle.hpPercent = float(vehicle_elem.get("hpp")) if vehicle_elem.get("hpp") is not None else 0.0
        vehicle.tox = float(vehicle_elem.get("tox")) if vehicle_elem.get("tox") is not None else 0.0
        vehicle.toy = float(vehicle_elem.get("toy")) if vehicle_elem.get("toy") is not None else 0.0

        self.objects[Vehicle].append(vehicle)

    def parse_water(self, water_elem):
        water_name = water_elem.get("uid")
        if water_name is None:
            raise ValueError("Water name cannot be empty or missing!")
        water = parse_map_object(Water,
                                 **fill_water_object_kwargs(water_name, water_elem))

        self.objects[Water].append(water)

    def parse_box(self, box_elem):
        self.objects[Box].append(parse_map_object(Box, **fill_box_object_kwargs(box_elem)))

    def parse_object(self, elem, obj_type):
        try:
            kwargs = {k: v for k, v in elem.attrib.items() if k != "type"}
            self.new_object(obj_type, **kwargs)
        except KeyError as e:
            print(f'Parsing error: {format_exc()}')
            # key = str(e)  # Get the key that caused the KeyError
            key_attempted = e.args[0]  # Get the specific key that was attempted
            value = elem.attrib.get(key_attempted, "N/A")  # Get the corresponding value or "N/A"
            print(f"Error creating object of type {obj_type}: KeyError for key '{key_attempted}' with value '{value}'")
            print(f"Element attributes: {elem.attrib}")

    def from_xml(self, xml_string: str):
        root = fromstring(xml_string)
        for object_type in self.objects.keys():
            for item in root.iter(object_type.__name__.lower()):
                self.parse_object(item, object_type)

    def find_trigger_by_name(self, name: str) -> Trigger:
        return find_object_by_name(self.objects[Trigger], "Trigger", name)

    def find_movable_by_name(self, name: str) -> Door:
        return find_object_by_name(self.objects[Door], "Door", name)

    def find_region_by_name(self, name: str) -> Region:
        return find_object_by_name(self.objects[Region], "Region", name)

    def find_pusher_by_name(self, name: str) -> Pushf:
        return find_object_by_name(self.objects[Pushf], "Pusher", name)

    def find_enemy_by_name(self, name: str) -> Enemy:
        return find_object_by_name(self.objects[Enemy], "Enemy", name)

    def find_player_by_name(self, name: str) -> Player:
        return find_object_by_name(self.objects[Player], "Player", name)

    def find_vehicle_by_name(self, name: str) -> Vehicle:
        return find_object_by_name(self.objects[Vehicle], "Vehicle", name)

    def find_decoration_by_name(self, name: str) -> Decor:
        return find_object_by_name(self.objects[Decor], "Decoration", name)

    def find_gun_by_name(self, name: str) -> Gun:
        return find_object_by_name(self.objects[Gun], "Gun", name)

    async def to_xml(self) -> str:
        # Convert the Map object to an XML string representation
        tasks = []

        for object_type, items in self.objects.items():
            for item in items:
                tasks.append(generate_item_xml(item))  # , object_type.__name__.lower()))

        results = await gather(*tasks)
        xml_content = ''.join(results)

        return xml_content


def find_object_by_name(obj_list, obj_type_str, name):
    for obj in obj_list:
        if obj.uid == name:
            return obj
    raise Exception(f"{obj_type_str} with name '{name}' not found.")


# Example of the generate_item_xml function (you need to define this function)
async def generate_item_xml(item):  # , field_name):
    return f'{item.to_xml}'
    # Logic to generate XML for the given item
    # Return the XML string representation of the item
    # return f'<{field_name}>{item.to_xml}</{field_name}>'


def parse_map_object(map_object: Union[type(Player), type(Enemy), type(Water), type(Box)], **kwargs):
    instance = map_object()
    for key, value in kwargs.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
    return instance


def fill_nameless_map_object_kwargs(ET_nameless_map_object) -> dict:
    return {
        "x": (int(ET_nameless_map_object.get("x")) if ET_nameless_map_object.get("x") is not None else 0),
        "y": (int(ET_nameless_map_object.get("y")) if ET_nameless_map_object.get("y") is not None else 0)
    }


def fill_named_map_object_kwargs(object_uid, ET_named_map_object) -> dict:
    return {
        **fill_nameless_map_object_kwargs(ET_named_map_object),
        "uid": object_uid
    }


# Box Only
def fill_box_object_kwargs(ET_box_object) -> dict:
    return {
        **fill_nameless_map_object_kwargs(ET_box_object),
        "w": (int(ET_box_object.get("w")) if
              ET_box_object.get("w") is not None else 0),
        "h": (int(ET_box_object.get("h")) if
              ET_box_object.get("h") is not None else 0),
        "m": (int(ET_box_object.get("m")) if
              ET_box_object.get("m") is not None else 0)
    }


# Water, Pusher, Door, Region Only
def fill_named_scaleable_object_kwargs(object_uid,
                                       ET_named_scaleable_map_object) -> dict:
    return {
        **fill_named_map_object_kwargs(object_uid, ET_named_scaleable_map_object),
        "w": (int(ET_named_scaleable_map_object.get("w")) if
              ET_named_scaleable_map_object.get("w") is not None else 0),
        "h": (int(ET_named_scaleable_map_object.get("h")) if
              ET_named_scaleable_map_object.get("h") is not None else 0)
    }


def fill_water_object_kwargs(water_uid,
                             ET_water_object) -> dict:
    return {
        **fill_named_scaleable_object_kwargs(water_uid, ET_water_object),
        "damage": (float(ET_water_object.get("damage"))
                   if ET_water_object.get("damage") is not None else 0),
        "friction": (ET_water_object.get("friction") == "true"
                     if ET_water_object.get("friction") is not None else "false")
    }


# Pusher, Door, Region Only
def fill_named_scaleable_attachable_object_kwargs(object_uid,
                                                  ET_named_scaleable_attachable_map_object) -> dict:
    return {
        **fill_named_scaleable_object_kwargs(object_uid, ET_named_scaleable_attachable_map_object),
        "attach": (str(ET_named_scaleable_attachable_map_object.get("attach"))
                   if ET_named_scaleable_attachable_map_object.get("attach") is not None else "-1")
    }


def fill_character_kwargs(character_uid, ET_player_or_enemy_object) -> dict:
    return {
        **fill_named_map_object_kwargs(character_uid, ET_player_or_enemy_object),
        "tox": (
            float(ET_player_or_enemy_object.get("tox")) if ET_player_or_enemy_object.get("tox") is not None else 0.0),
        "toy": (
            float(ET_player_or_enemy_object.get("toy")) if ET_player_or_enemy_object.get("toy") is not None else 0.0),
        "hea": (
            float(ET_player_or_enemy_object.get("hea")) if ET_player_or_enemy_object.get("hea") is not None else 0.0),
        "hmax": (float(ET_player_or_enemy_object.get("hmax")) if ET_player_or_enemy_object.get(
            "hmax") is not None else 0.0),
        "team": (
            int(ET_player_or_enemy_object.get("team")) if ET_player_or_enemy_object.get("team") is not None else 0),
        "side": (
            int(ET_player_or_enemy_object.get("side")) if ET_player_or_enemy_object.get("side") is not None else 0),
        "char": (
            int(ET_player_or_enemy_object.get("char")) if ET_player_or_enemy_object.get("char") is not None else 0),
        "botaction": (int(ET_player_or_enemy_object.get("botaction")) if ET_player_or_enemy_object.get(
            "botaction") is not None else 0),
        "ondeath": (str(ET_player_or_enemy_object.get("ondeath")) or "-1"),
        "incar": (str(ET_player_or_enemy_object.get("incar")) or "-1")
    }
