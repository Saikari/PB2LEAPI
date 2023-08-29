"""
MapObjectSpecials Module

This module defines classes and constants that encapsulate various aspects of a game engine.
It provides color options for displayed text actions, activation types for regions,
and marks for different engine features.

Classes:
    ShownTextActionColor:
        Represents color options for shown text actions.

    RegionActivationType:
        Represents region activation types.

    EngineMarks:
        Represents various engine marks for different features.

Usage Examples:
    # Import the classes and constants
    from engine_constants import ShownTextActionColor, RegionActivationType, EngineMarks

    # Use color constants for text actions
    hero_color = ShownTextActionColor.HERO
    proxy_color = ShownTextActionColor.PROXY

    # Access region activation types
    button_activation = RegionActivationType.BUTTON
    player_activation = RegionActivationType.BY_PLAYER

    # Utilize engine marks
    sky_change_mark = EngineMarks.CHANGE_SKY
    marine_weapons_mark = EngineMarks.MARINE_WEAPONS
"""


class ShownTextActionColor:
    """
    Represents color options for shown text actions.

    Attributes:
        EXOS (str): EXOS color code "0".
        HERO (str): HERO color code "1".
        NOIR_LIME (str): NOIR_LIME color code "2".
        PROXY (str): PROXY color code "3".
        CIVIL_SECURITY (str): CIVIL_SECURITY color code "4".

    Args:
        value (str): The input color value to validate.

    Raises:
        ValueError: If the input value is not a valid color option.

    Methods:
        validate_input(input_value): Validates the input color value.

    """
    EXOS = "0"
    HERO = "1"
    NOIR_LIME = "2"
    PROXY = "3"
    CIVIL_SECURITY = "4"

    def __init__(self, value):
        self.color = self.validate_input(value)

    def validate_input(self, input_value):
        """
        Validate the input color value.

        Args:
            input_value (str): The input color value to validate.

        Returns:
            str: Validated color value.

        Raises:
            ValueError: If the input value is not a valid color option.

        """
        if input_value in [self.EXOS, self.HERO, self.NOIR_LIME, self.PROXY, self.CIVIL_SECURITY]:
            return input_value

        hex_pattern = compile(r'^#[0-9A-Fa-f]{6}$')
        if hex_pattern.match(input_value):
            return input_value
        raise ValueError("Invalid input value.")


class RegionActivationType:
    """
    Represents region activation types.

    Constants:
        NOTHING (int): Nothing activation type.
        BUTTON (int): Button activation type.
        BY_CHAR_NOT_IN_VEHICLE (int): Activation by character not in vehicle.
        BY_CHAR_IN_VEHICLE (int): Activation by character in vehicle.
        BY_CHAR (int): Activation by character.
        BY_MOVABLE (int): Activation by movable object.
        BY_PLAYER (int): Activation by player.
        BY_ALL_HERO (int): Activation by all heroes.
        INVISIBLE_BUTTON (int): Invisible button activation type.
        RED_BUTTON (int): Red button activation type.
        BLUE_BUTTON (int): Blue button activation type.
        INVISIBLE_RED_BUTTON (int): Invisible red button activation type.
        INVISIBLE_BLUE_BUTTON (int): Invisible blue button activation type.
        BY_RED_PLAYER (int): Activation by red team player.
        BY_BLUE_PLAYER (int): Activation by blue team player.
        INVISIBLE_BUTTON_WITHOUT_SOUND (int): Invisible button activation type without sound.

    """
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
    """
    Represents various engine marks for different features.

    Constants:
        CHANGE_SKY (str): Change sky mark.
        SHADOW_MAP_SIZE (str): Shadow map size mark.
        CASUAL_MODE (str): Casual mode mark.
        NO_BASE_NOISE (str): No base noise mark.
        ALT_GAME (str): Alternate game mark.
        STRICT_CASUAL_MODE (str): Strict casual mode mark.
        NO_AUTO_REVIVE (str): No auto-revive mark.
        FORCE_RAGDOLL_DISAPPEARANCE (str): Force ragdoll disappearance mark.
        MARINE_WEAPONS (str): Marine weapons mark.
        PROXY_WEAPONS (str): Proxy weapons mark.
        PROXY_WEAPONS_NO_NADE (str): Proxy weapons mark without grenades.
        PROXY_WEAPONS_ONLY_NADES (str): Proxy weapons mark with only grenades.
        NO_PSI (str): No PSI mark.
        GAME_SCALE (str): Game scale mark.
        HE_NADES_COUNT (str): HE grenades count mark.
        PORT_NADES_COUNT (str): Portable grenades count mark.
        SH_NADES_COUNT (str): Shock grenades count mark.
        SNOW (str): Snow mark.
        WATER_COLOR (str): Water color mark.
        ACID_COLOR (str): Acid color mark.
        WATER_TITLE (str): Water title mark.
        ACID_TITLE (str): Acid title mark.
        SLOTS_ON_SPAWN (str): Slots on spawn mark.
        MAX_GUNS_ON_SPAWN (str): Max guns on spawn mark.
        TRIGGER_ERROR_REPORTING (str): Trigger error reporting mark.
        VAR_SYNC_ACTIONS (str): Variable synchronization actions mark.
        NO_LIGHT_BREAK (str): No light break mark.
        NAIVE_HIT_CONFIRMATION (str): Naive hit confirmation mark.

    """
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
