from re import compile


class ShownTextColor:
    EXOS = "0"
    HERO = "1"
    NOIR_LIME = "2"
    PROXY = "3"
    CIVIL_SECURITY = "4"

    def __init__(self, value):
        self.color = self.validate_input(value)

    def validate_input(self, input_value):
        if input_value in [self.EXOS, self.HERO, self.NOIR_LIME, self.PROXY, self.CIVIL_SECURITY]:
            return input_value

        hex_pattern = compile(r'^#[0-9A-Fa-f]{6}$')
        if hex_pattern.match(input_value):
            return input_value
        raise ValueError("Invalid input value.")


class RegionActivation:
    NOTHING = -1
    BUTTON = 1
    BY_CHAR_NOT_IN_VEHICLE = 2
    BY_CHAR_IN_VEHICLE = 3
    BY_CHAR = 4
    BY_MOVABLE = 5
    BY_PLAYER = 6
    BY_ALL_HERO = 7
    INVISIBLE_BUTTON = 8
    RED_BUTTON = 9
    BLUE_BUTTON = 10
    INVISIBLE_RED_BUTTON = 11
    INVISIBLE_BLUE_BUTTON = 12
    BY_RED_PLAYER = 13
    BY_BLUE_PLAYER = 14
    INVISIBLE_BUTTON_WITHOUT_SOUND = 15


class EngineMarks:
    CHANGE_SKY = "sky"
    SHADOW_MAP_SIZE = "shadowmap_size"
    CASUAL_MODE = "casual"
    NO_BASE_NOISE = "nobase"
    ALT_GAME = "game2"
    STRICT_CASUAL_MODE = "strict_casual"
    NO_AUTO_REVIVE = "no_auto_revive"
    FORCE_RAGDOLL_DISAPPEARANCE = "meat"
    MARINE_WEAPONS = "hero1_guns"
    PROXY_WEAPONS = "hero2_guns"
    PROXY_WEAPONS_NO_NADE = "hero2_guns_nonades"
    PROXY_WEAPONS_ONLY_NADES = "hero2_guns_nades"
    NO_PSI = "nopsi"
    GAME_SCALE = "gamescale"
    HE_NADES_COUNT = "he_nades_count"
    PORT_NADES_COUNT = "port_nades_count"
    SH_NADES_COUNT = "sh_nades_count"
    SNOW = "snow"
    WATER_COLOR = "watercolor"
    ACID_COLOR = "acidcolor"
    WATER_TITLE = "watertitle"
    ACID_TITLE = "acidtitle"
    SLOTS_ON_SPAWN = "dm_slots_on_spawn"
    MAX_GUNS_ON_SPAWN = "dm_max_guns_on_spawn"
    TRIGGER_ERROR_REPORTING = "level_errors"
    VAR_SYNC_ACTIONS = "var_sync"
    NO_LIGHT_BREAK = "no_light_break"
    NAIVE_HIT_CONFIRMATION = "naive_hit_confirmation"
