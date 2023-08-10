from re import sub
from typing import Optional
from aiofiles import open
from DataInterfaces.Map import Map
from os import path

class MapIO:
    @staticmethod
    async def read_file_async(file_location: str) -> str:
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
            raise Exception(f"Error decoding file '{file_location}' as UTF-8: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while reading the file: {e}")

    @staticmethod
    async def load_map_from_object_async(file_location: str) -> Optional[Map]:
        try:
            map_instance = Map()
            map_instance.from_xml('<?xml version="1.0" encoding="UTF-8" ?><root>'
                                  f'{await MapIO.read_file_async(file_location) if path.isfile(file_location) else file_location}</root>')
            return map_instance
        except FileNotFoundError as e:
            raise Exception(f"Could not find the file '{file_location}': {e}")
        except PermissionError as e:
            raise Exception(f"Permission denied to read the file '{file_location}': {e}")
        except IsADirectoryError as e:
            raise Exception(f"'{file_location}' is a directory, not a file: {e}")
        except UnicodeDecodeError as e:
            raise Exception(f"Error decoding file '{file_location}' as UTF-8: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while loading the map: {e}")

    @staticmethod
    async def write_to_file_async(file_location: str, content: str):
        try:
            async with open(file_location, 'w') as f:
                await f.write(content)
        except FileNotFoundError as e:
            raise Exception(f"Could not find the file '{file_location}': {e}")
        except PermissionError as e:
            raise Exception(f"Permission denied to write to the file '{file_location}': {e}")
        except IsADirectoryError as e:
            raise Exception(f"'{file_location}' is a directory, cannot write: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while writing to the file: {e}")

    @staticmethod
    async def dump_map_async(map_instance: Map, file_location: str):
        try:
            await MapIO.write_to_file_async(file_location, await map_instance.to_xml())
        except FileNotFoundError as e:
            raise Exception(f"Could not find the file '{file_location}' to write the map: {e}")
        except PermissionError as e:
            raise Exception(f"Permission denied to write to the file '{file_location}': {e}")
        except IsADirectoryError as e:
            raise Exception(f"'{file_location}' is a directory, cannot write: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while dumping the map: {e}")
