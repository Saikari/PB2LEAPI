"""
Entity Module

This module defines classes representing various game entities and actions within a game.
It includes classes for nameless and named map object entities, image entities,
and trigger actions. Additionally, it defines a core action used in PB2 Triggers.

Classes:
    NamelessMapObjectEntity:
        Represents a nameless map object entity.

    ImageEntity:
        Represents an image entity.

    NamedMapObjectEntity:
        Represents a named map object entity, inheriting from NamelessMapObjectEntity.

    TriggersActionEntity:
        Represents an action within a trigger.

Constants:
    DO_NOTHING:
        A core action used in PB2 Triggers that represents doing nothing.

Usage Example:
    # Import the classes and constant
    from game_entities import (
        NamelessMapObjectEntity,
        ImageEntity,
        NamedMapObjectEntity,
        TriggersActionEntity,
        DO_NOTHING,
    )

    # Create instances of the defined classes
    nameless_entity = NamelessMapObjectEntity(x=10, y=20)
    image = ImageEntity(width=100, height=200, id=1)
    named_entity = NamedMapObjectEntity(x=30, y=40, uid="entity_123")
    action = TriggersActionEntity(opID=5, args=[arg1, arg2])

    # Use the DO_NOTHING action
    trigger_action = DO_NOTHING
"""


class NamelessMapObjectEntity:
    """
    Represents a nameless map object entity.

    Attributes:
        x (int): The X-coordinate of the map object.
        y (int): The Y-coordinate of the map object.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def print_all_fields(self):
        print(", ".join([f"{key}: {value}" for key, value in self.__dict__.items()]))


class ImageEntity:
    """
    Represents an image entity.

    Attributes:
        width (int): The width of the image.
        height (int): The height of the image.
        id (int): The ID of the image.
    """

    def __init__(self, width=0, height=0, id=0):
        self.width = width
        self.height = height
        self.id = id

    def print_all_fields(self):
        print(", ".join([f"{key}: {value}" for key, value in self.__dict__.items()]))


class NamedMapObjectEntity(NamelessMapObjectEntity):
    """
    Represents a named map object entity, inheriting from NamelessMapObjectEntity.

    Attributes:
        x (int): The X-coordinate of the map object.
        y (int): The Y-coordinate of the map object.
        uid (str): The unique identifier of the map object.
    """

    def __init__(self, x=0, y=0, uid=""):
        super().__init__(x, y)
        self.uid = uid

    def print_all_fields(self):
        print(", ".join([f"{key}: {value}" for key, value in self.__dict__.items()]))


class TriggersActionEntity:
    """
    Represents an action within a trigger.

    Attributes:
        opID (int): The operation ID of the action.
        args (list): The list of arguments for the action.
    """

    def __init__(self, opID=0, args=None):
        if args is None:
            args = []
        self.opID = opID
        self.args = args


# Most used Action at PB2 Triggers Literally the core of whole game
DO_NOTHING = TriggersActionEntity(opID=-1, args=[])
