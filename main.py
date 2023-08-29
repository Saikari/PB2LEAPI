"""
Asynchronous Map Loading and Dumping Example

This script demonstrates asynchronous loading and dumping of map instances using the MapIO class.
It uses asyncio and logging to showcase how to load a map from a file, modify it, and then asynchronously
dump it back to a file.

Usage:
    - Ensure you have the MapIO module with the required functions.
    - Make sure to have the 'XML/bossfight_map1.xml' file for loading.
    - The modified map instance is then dumped into 'output.xml'.

Example Usage:
    # Import required modules
    from asyncio import run
    from logging import basicConfig, error, DEBUG, info
    from DataInterfaces.MapIO import MapIO

    # Set up logging configuration
    basicConfig(
        level=DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Example usage
    async def main():
        try:
            map_instance = await MapIO.load_map_from_file_async("XML/bossfight_map1.xml")
            info("Map loaded successfully!")
            info("Map instance has been created successfully!")
            # Assuming you have a map_instance created and modified
            await MapIO.dump_map_async(map_instance, "output.xml")
            info("Map dumped and written to file asynchronously!")

        except Exception as e:
            error(f"Error: {e}", exc_info=True)

    if __name__ == "__main__":
        run(main())
"""

# This script demonstrates asynchronous loading and dumping of map instances using the MapIO class.
# It uses asyncio and logging to showcase how to load a map from a file, modify it, and then asynchronously
# dump it back to a file.

# Usage:
#     - Ensure you have the MapIO module with the required functions.
#     - Make sure to have the 'XML/bossfight_map1.xml' file for loading.
#     - The modified map instance is then dumped into 'output.xml'.

from asyncio import run
from logging import basicConfig, error, DEBUG, info

from DataInterfaces.MapIO import MapIO
from DataInterfaces.MapObjects import Player


# Set up logging configuration
basicConfig(
    level=DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize map tools
mapTools = MapTools()


# Example usage
async def main():
    """
    Asynchronous Map Loading and Dumping Entry Point

    This function serves as the entry point for an asynchronous process of loading a map
    from a file, modifying it, and then asynchronously dumping it back to a file.
    It demonstrates the usage of the MapIO class with async operations and logging.

    Raises:
        Exception: If an error occurs during map loading, modification, or dumping.

    Example Usage:
        # Import required modules
        from asyncio import run
        from logging import error, info
        from DataInterfaces.MapIO import MapIO

        # Example usage
        if __name__ == "__main__":
            try:
                run(main())
            except Exception as e:
                error(f"Error: {e}", exc_info=True)
    """
    try:
        map_instance = await MapIO.load_map_from_file_async("XML/bossfight_map1.xml")
        info("Map loaded successfully!")
        info("Map instance has been created successfully!")
        for i in map_instance.objects[Player]:
            i.print_all_fields()
        # Assuming you have a map_instance created and modified
        await MapIO.dump_map_async(map_instance, "output.xml")
        info("Map dumped and written to file asynchronously!")

    except Exception as e:
        error(f"Error: {e}", exc_info=True)


if __name__ == "__main__":
    run(main())
