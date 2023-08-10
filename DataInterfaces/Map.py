import re
from asyncio import gather
from itertools import chain
from xml.etree.ElementTree import fromstring

from DataInterfaces.Entity import Action
from DataInterfaces.MapObjectSpecials import EngineMarks
from DataInterfaces.MapObjects import Door, Region, Timer, Vehicle, Box, Water, Decoration, Song, Lamp, Barrel, Gun, \
    Pusher, Background, Character, EngineMark, Trigger
from traceback import format_exc

class Map:
    def __init__(self):
        self.objects = {
            Door: [],
            Region: [],
            Timer: [],
            Vehicle: [],
            Box: [],
            Water: [],
            Decoration: [],
            Song: [],
            Lamp: [],
            Barrel: [],
            Gun: [],
            Pusher: [],
            Background: [],
            Character: [],
            EngineMark: [],
            Trigger: []
        }

    def new_object(self, obj_type, **kwargs):
        result = obj_type(**kwargs)
        self.objects[obj_type].append(result)

    def new_movable(self, name, x, y, w, h, tarx, tary=0, speed=10, visible=True, moving=False, attachTo=None):
        self.new_object(Door, name=name, x=x, y=y, w=w, h=h, tarx=tarx, tary=tary, speed=speed, visible=visible,
                        moving=moving, attachTo=attachTo)

    def new_region(self, name, x, y, w, h=0, actTrigger=None, actOn=None, attachTo=None):
        self.new_object(Region, name=name, x=x, y=y, w=w, h=h, actTrigger=actTrigger, actOn=actOn, attachTo=attachTo)

    def new_timer(self, name, x, y=0, enabled=True, callback=None, maxCalls=1, delay=30):
        self.new_object(Timer, name=name, x=x, y=y, enabled=enabled, callback=callback, maxCalls=maxCalls, delay=delay)

    def new_vehicle(self, model="veh_jeep", x=0, y=0, tox=0, toy=0, side=1, hpPercent=100):
        self.new_object(Vehicle, model=model, x=x, y=y, tox=tox, toy=toy, side=side, hpPercent=hpPercent)

    def new_box(self, x, y, w, h, material=0):
        self.new_object(Box, x=x, y=y, w=w, h=h, material=material)

    def new_water(self, x, y, w, h, damage=0, friction=True):
        self.new_object(Water, x=x, y=y, w=w, h=h, damage=damage, friction=friction)

    def new_decoration(self, name, x, y, texX, texY, rotation, layer=0, scaleX=1, scaleY=1, model="stone",
                       attachTo=None):
        self.new_object(Decoration, name=name, x=x, y=y, texX=texX, texY=texY, rotation=rotation, layer=layer,
                        scaleX=scaleX, scaleY=scaleY, model=model, attachTo=attachTo)

    def new_song(self, name, x, y=0, url="", volume=1, loop=True, onEnd=None):
        self.new_object(Song, name=name, x=x, y=y, url=url, volume=volume, loop=loop, onEnd=onEnd)

    def new_lamp(self, name, x, y=0, power=0.4, hasFlare=True):
        self.new_object(Lamp, name=name, x=x, y=y, power=power, hasFlare=hasFlare)

    def new_barrel(self, name, x, y, tox, toy=0, model="bar_orange"):
        self.new_object(Barrel, name=name, x=x, y=y, tox=tox, toy=toy, model=model)

    def new_weapon(self, name, x, y, level=0, team=-1, model="gun_rifle"):
        self.new_object(Gun, name=name, x=x, y=y, level=level, team=team, model=model)

    def new_pusher(self, name, x, y, tox, toy, stabilityDamage, damage=0, attachTo=None):
        self.new_object(Pusher, name=name, x=x, y=y, tox=tox, toy=toy, stabilityDamage=stabilityDamage, damage=damage,
                        attachTo=attachTo)

    def new_background(self, x, y, texX, texY, layer=0, hexMultiplier="", showShadow=True, attachTo=None):
        self.new_object(Background, x=x, y=y, texX=texX, texY=texY, layer=layer, hexMultiplier=hexMultiplier,
                        showShadow=showShadow, attachTo=attachTo)

    def new_character(self, name, x, y, tox, toy=0, hea=130, hmax=130, team=0, side=1, skin=-1, incar=None, botAction=4,
                      onDeath=None, isPlayer=True):
        self.new_object(Character, name=name, x=x, y=y, tox=tox, toy=toy, hea=hea, hmax=hmax, team=team, side=side,
                        skin=skin, botAction=botAction, onDeath=onDeath, isPlayer=isPlayer, incar=incar)

    def new_engine_mark(self, x, y=0, modifier=EngineMarks.MARINE_WEAPONS, parameter="0"):
        self.new_object(EngineMark, x=x, y=y, modifier=modifier, parameter=parameter)

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
            action = Action()
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

    def parse_character(self, character_elem):
        character = Character()

        character_name = character_elem.get("uid")
        if character_name is None:
            raise ValueError("Character name cannot be empty or missing!")
        character.uid = str(character_name)

        character.x = int(character_elem.get("x")) if character_elem.get("x") is not None else 0
        character.y = int(character_elem.get("y")) if character_elem.get("y") is not None else 0
        character.isPlayer = bool(character_elem.find("player") is not None)

        character.tox = float(character_elem.get("tox")) if character_elem.get("tox") is not None else 0.0
        character.toy = float(character_elem.get("toy")) if character_elem.get("toy") is not None else 0.0
        character.hea = float(character_elem.get("hea")) if character_elem.get("hea") is not None else 0.0
        character.hmax = float(character_elem.get("hmax")) if character_elem.get("hmax") is not None else 0.0

        character.team = int(character_elem.get("team")) if character_elem.get("team") is not None else 0
        character.side = int(character_elem.get("side")) if character_elem.get("side") is not None else 0
        character.char = int(character_elem.get("skin")) if character_elem.get("skin") is not None else 0
        character.botaction = int(character_elem.get("botaction")) if character_elem.get("botaction") is not None else 0
        character.ondeath = str(character_elem.get("ondeath")) or ""

        self.objects[Character].append(character)

    def parse_door(self, door_elem):
        door = Door()

        movable_name = str(door_elem.get("uid"))
        if movable_name is None or movable_name.strip() == "":
            raise ValueError("Movable name cannot be empty or missing!")
        door.uid = str(movable_name)

        door.w = int(door_elem.get("w")) if door_elem.get("w") is not None else 0
        door.h = int(door_elem.get("h")) if door_elem.get("h") is not None else 0
        door.y = int(door_elem.get("y")) if door_elem.get("y") is not None else 0
        door.x = int(door_elem.get("x")) if door_elem.get("x") is not None else 0
        door.maxspeed = float(door_elem.get("maxspeed")) if door_elem.get("maxspeed") is not None else 0.0
        door.vis = bool(door_elem.get("vis") == "true")
        door.attach = str(door_elem.get("attach")) or ""

        self.objects[Door].append(door)

    def parse_decoration(self, decoration_elem):
        decoration = Decoration()

        decoration_name = decoration_elem.get("uid")
        if decoration_name is None or decoration_name.strip() == "":
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

        decoration.attach = str(decoration_elem.get("attach")) or ""

        self.objects[Decoration].append(decoration)

    def parse_region(self, region_elem):
        region = Region()

        region_name = region_elem.get("uid")
        if region_name is None or region_name.strip() == "":
            raise ValueError("Region name cannot be empty or missing!")
        region.uid = str(region_name)

        region.x = int(region_elem.get("x")) if region_elem.get("x") is not None else 0
        region.y = int(region_elem.get("y")) if region_elem.get("y") is not None else 0
        region.h = int(region_elem.get("h")) if region_elem.get("h") is not None else 0
        region.w = int(region_elem.get("w")) if region_elem.get("w") is not None else 0

        region.use_on = int(region_elem.get("use_on")) if region_elem.get("use_on") is not None else 0
        region.use_target = region_elem.get("use_target") if region_elem.get("use_target") is not None else ""

        region.attach = region_elem.get("attach") or ""

        self.objects[Region].append(region)

    def parse_song(self, song_elem):
        song = Song()

        song_name = song_elem.get("uid")
        if song_name is None or song_name.strip() == "":
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
        if lamp_name is None or lamp_name.strip() == "":
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
        if barrel_name is None or barrel_name.strip() == "":
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
        if weapon_name is None or weapon_name.strip() == "":
            raise ValueError("Gun name cannot be empty or missing!")
        gun.uid = str(weapon_name)

        gun.x = int(gun_elem.get("x")) if gun_elem.get("x") is not None else 0
        gun.y = int(gun_elem.get("y")) if gun_elem.get("y") is not None else 0
        gun.command = int(gun_elem.get("command")) if gun_elem.get("command") is not None else 0
        gun.upg = int(gun_elem.get("upg")) if gun_elem.get("upg") is not None else 0

        gun.model = str(gun_elem.get("model"))

        self.objects[Gun].append(gun)

    def parse_pusher(self, pusher_elem):
        pusher = Pusher()

        pusher_name = pusher_elem.get("name")
        if pusher_name is None or pusher_name.strip() == "":
            raise ValueError("Pusher name cannot be empty or missing!")
        pusher.uid = str(pusher_name)

        pusher.x = int(pusher_elem.get("x")) if pusher_elem.get("x") is not None else 0
        pusher.y = int(pusher_elem.get("y")) if pusher_elem.get("y") is not None else 0
        pusher.h = int(pusher_elem.get("h")) if pusher_elem.get("h") is not None else 0
        pusher.w = int(pusher_elem.get("w")) if pusher_elem.get("w") is not None else 0
        pusher.tox = float(pusher_elem.get("tox")) if pusher_elem.get("tox") is not None else 0.0
        pusher.toy = float(pusher_elem.get("toy")) if pusher_elem.get("toy") is not None else 0.0
        pusher.attachTo = pusher_elem.get("attach") or ""
        pusher.damage = float(pusher_elem.get("damage")) if pusher_elem.get("damage") is not None else 0.0
        pusher.stabilityDamage = float(pusher_elem.get("stab")) if pusher_elem.get("stab") is not None else 0.0

        self.objects[Pusher].append(pusher)

    def parse_vehicle(self, vehicle_elem):
        vehicle = Vehicle()

        vehicle_name = vehicle_elem.get("name")
        if vehicle_name is None or vehicle_name.strip() == "":
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
        water = Water()

        water_name = water_elem.get("name")
        if water_name is None or water_name.strip() == "":
            raise ValueError("Water name cannot be empty or missing!")
        water.uid = str(water_name)

        water.x = int(water_elem.get("x"))
        water.y = int(water_elem.get("y"))
        water.w = int(water_elem.get("w"))
        water.h = int(water_elem.get("h"))

        water.damage = float(water_elem.get("damage"))

        water.friction = water_elem.get("friction") == "True"

        self.objects[Water].append(water)

    def parse_box(self, box_elem):
        box = Box()

        box.h = int(box_elem.get("h"))
        box.w = int(box_elem.get("w"))
        box.x = int(box_elem.get("x"))
        box.y = int(box_elem.get("y"))
        box.m = int(box_elem.get("m"))

        self.objects[Box].append(box)

    def parse_object(self, elem, obj_type):
        try:
            kwargs = {k: v for k, v in elem.attrib.items() if k != "type"}
            self.new_object(obj_type, **kwargs)
        except KeyError as e:
            print(f'Parsing error: {format_exc()}')
            key = str(e)  # Get the key that caused the KeyError
            key_attempted = e.args[0]  # Get the specific key that was attempted
            value = elem.attrib.get(key_attempted, "N/A")  # Get the corresponding value or "N/A"
            print(f"Error creating object of type {obj_type}: KeyError for key '{key_attempted}' with value '{value}'")
            print(f"Element attributes: {elem.attrib}")

    def from_xml(self, xml_string: str):
        print(xml_string)
        root = fromstring(xml_string)
        for trigger_elem in root.iter("trigger"):
            self.parse_object(trigger_elem, Trigger)

        for timer_elem in root.iter("timer"):
            self.parse_object(timer_elem, Timer)

        for character_elem in chain(root.iter("actor"), root.iter("player")):
            self.parse_object(character_elem, Character)

        for movable_elem in root.iter("door"):
            self.parse_object(movable_elem, Door)

        for decoration_elem in root.iter("decor"):
            self.parse_object(decoration_elem, Decoration)

        for region_elem in root.iter("region"):
            self.parse_object(region_elem, Region)

        for song_elem in root.iter("song"):
            self.parse_object(song_elem, Song)

        for lamp_elem in root.iter("lamp"):
            self.parse_object(lamp_elem, Lamp)

        for barrel_elem in root.iter("barrel"):
            self.parse_object(barrel_elem, Barrel)

        for weapon_elem in root.iter("gun"):
            self.parse_object(weapon_elem, Gun)

        for pusher_elem in root.iter("pusher"):
            self.parse_object(pusher_elem, Pusher)

        for vehicle_elem in root.iter("vehicle"):
            self.parse_object(vehicle_elem, Vehicle)

        for water_elem in root.iter("water"):
            self.parse_object(water_elem, Water)

        for box_elem in root.iter("box"):
            self.parse_object(box_elem, Box)

    @staticmethod
    def find_object_by_name(obj_list, obj_type_str, name):
        for obj in obj_list:
            if obj.uid == name:
                return obj
        raise Exception(f"{obj_type_str} with name '{name}' not found.")

    def find_trigger_by_name(self, name: str) -> Trigger:
        return self.find_object_by_name(self.objects[Trigger], "Trigger", name)

    def find_movable_by_name(self, name: str) -> Door:
        return self.find_object_by_name(self.objects[Door], "Door", name)

    def find_region_by_name(self, name: str) -> Region:
        return self.find_object_by_name(self.objects[Region], "Region", name)

    def find_pusher_by_name(self, name: str) -> Pusher:
        return self.find_object_by_name(self.objects[Pusher], "Pusher", name)

    def find_character_by_name(self, name: str) -> Character:
        return self.find_object_by_name(self.objects[Character], "Character", name)

    def find_vehicle_by_name(self, name: str) -> Vehicle:
        return self.find_object_by_name(self.objects[Vehicle], "Vehicle", name)

    def find_decoration_by_name(self, name: str) -> Decoration:
        return self.find_object_by_name(self.objects[Decoration], "Decoration", name)

    def find_gun_by_name(self, name: str) -> Gun:
        return self.find_object_by_name(self.objects[Gun], "Gun", name)

    async def to_xml(self) -> str:
        # Convert the Map object to an XML string representation
        tasks = []

        for object_type, items in self.objects.items():
            for item in items:
                tasks.append(generate_item_xml(item))  # , object_type.__name__.lower()))

        results = await gather(*tasks)
        xml_content = ' '.join(results)

        xml = re.sub(r'(\w+)\s*=\s*([^\s>]+)',
                     lambda match: f'{match.group(1)}="{match.group(2)}"' if '"' not in match.group(2) else match.group(
                         0), xml_content)

        return re.sub(r'\s{2,}', ' ', xml)


# Example of the generate_item_xml function (you need to define this function)
async def generate_item_xml(item): ###, field_name):
    return f'{item.to_xml}'
    # Logic to generate XML for the given item
    # Return the XML string representation of the item
    #return f'<{field_name}>{item.to_xml}</{field_name}>'
