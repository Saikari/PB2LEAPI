"""
MapIO Module

This module provides utility functions for reading and writing Map objects from and to files asynchronously.
It leverages the aiofiles library for asynchronous file operations and works with
Map instances from the DataInterfaces package.

Classes:
    MapIO:
        A utility class for asynchronous file operations related to Map instances.

Note:
    This module assumes that the 'Map' class is defined in the 'DataInterfaces.Map' module.

Usage Example:
    # Import the MapIO class
    from map_io_module import MapIO

    # Load a Map instance from a file asynchronously
    map_instance = await MapIO.load_map_from_file_async('map.xml')

    # Modify the Map instance

    # Dump the Map instance back to the file asynchronously
    await MapIO.dump_map_async(map_instance, 'modified_map.xml')
"""
from typing import Optional

from aiofiles import open

from DataInterfaces.Map import Map
from os import path

class MapIO:
    """
    A utility class for reading and writing map files.

    Methods:
        read_file_async(file_location: str) -> str:
            Reads a file asynchronously and returns its content as a string.

        load_map_from_file_async(file_location: str) -> Optional[Map]:
            Loads a Map instance from a file asynchronously.

        write_to_file_async(file_location: str, content: str):
            Writes content to a file asynchronously.

        dump_map_async(map_instance: Map, file_location: str):
            Dumps a Map instance to a file asynchronously.
    """

    @staticmethod
    async def read_file_async(file_location: str) -> str:
        """
        Read a file asynchronously and return its content as a string.

        Args:
            file_location (str): The path to the file to be read.

        Returns:
            str: The content of the file as a string.

        Raises:
            FileNotFoundError: If the file is not found.
            PermissionError: If permission is denied to read the file.
            IsADirectoryError: If the given path points to a directory.
            UnicodeDecodeError: If there is an error decoding the file as UTF-8.
            Exception: If any other error occurs while reading the file.
        """

        try:
            async with open(file_location, 'r') as f:
                return await f.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Could not find the file '{file_location}'. Error: {e}")
        except PermissionError as e:
            raise PermissionError(f"Permission denied to read the file '{file_location}'. Error: {e}")
        except IsADirectoryError as e:
            raise IsADirectoryError(f"'{file_location}' is a directory, not a file. Error: {e}")
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(e.encoding, e.object, e.start, e.end,
                                     f"Error decoding file '{file_location}' as UTF-8: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while reading the file: {e}")

    @staticmethod
    async def load_map_from_file_async(file_location: str) -> Optional[Map]:
        """
        Load a Map instance from a file asynchronously.

        This method reads XML content from the specified file location, constructs a Map instance,
        and populates it with data from the XML content.

        Args:
            file_location (str): The path to the file containing the map data.

        Returns:
            Optional[Map]: A Map instance loaded from the file, or None if loading fails.

        Raises:
            FileNotFoundError: If the file is not found at the specified location.
            PermissionError: If permission is denied to read the file.
            IsADirectoryError: If the specified location points to a directory instead of a file.
            UnicodeDecodeError: If there is an error decoding the file as UTF-8.
            Exception: If any other error occurs while loading the map.
        """

        try:
            map_instance = Map()
            map_instance.from_xml('<?xml version="1.0" encoding="UTF-8" ?><root>'
                                  f'{await MapIO.read_file_async(file_location) if path.isfile(file_location) else file_location}</root>')
            return map_instance
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Could not find the file '{file_location}': {e}")
        except PermissionError as e:
            raise PermissionError(f"Permission denied to read the file '{file_location}': {e}")
        except IsADirectoryError as e:
            raise IsADirectoryError(f"'{file_location}' is a directory, not a file: {e}")
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(e.encoding, e.object, e.start, e.end,
                                     f"Error decoding file '{file_location}' as UTF-8: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while loading the map: {e}")

    @staticmethod
    async def write_to_file_async(file_location: str, content: str):
        """
        Write content to a file asynchronously.

        Args:
            file_location (str): The path to the file to be written.
            content (str): The content to write to the file.

        Raises:
            FileNotFoundError: If the file is not found.
            PermissionError: If permission is denied to write to the file.
            IsADirectoryError: If the given path points to a directory.
            Exception: If any other error occurs while writing to the file.
        """
        try:
            async with open(file_location, 'w') as f:
                await f.write(content)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Could not find the file '{file_location}': {e}")
        except PermissionError as e:
            raise PermissionError(f"Permission denied to write to the file '{file_location}': {e}")
        except IsADirectoryError as e:
            raise IsADirectoryError(f"'{file_location}' is a directory, cannot write: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while writing to the file: {e}")

    @staticmethod
    async def dump_map_async(map_instance: Map, file_location: str):
        """
        Dump a Map instance to a file asynchronously.

        Args:
            map_instance (Map): The Map instance to be dumped.
            file_location (str): The path to the file where the map data will be written.

        Raises:
            FileNotFoundError: If the file is not found.
            PermissionError: If permission is denied to write to the file.
            IsADirectoryError: If the given path points to a directory.
            Exception: If any other error occurs while dumping the map.
        """
        try:
            await MapIO.write_to_file_async(file_location, await map_instance.to_xml())
        except FileNotFoundError as e:
            raise Exception(f"Could not find the file '{file_location}' to write the map: {e}")
        except PermissionError as e:
            raise PermissionError(f"Permission denied to write to the file '{file_location}': {e}")
        except IsADirectoryError as e:
            raise IsADirectoryError(f"'{file_location}' is a directory, cannot write: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while dumping the map: {e}")
