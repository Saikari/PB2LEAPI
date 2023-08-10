import logging
from asyncio import run

from DataInterfaces.MapIO import MapIO

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Example usage
async def main():
    try:
        map_instance = await MapIO.load_map_from_file_async("XML/bossfight_map1.xml")
        logging.info("Map loaded successfully!")
        logging.debug(map_instance)  # Use logging.debug for more detailed information
        logging.info("Map instance has been created successfully!")

        # Assuming you have a map_instance created and modified
        await MapIO.dump_map_async(map_instance, "output.xml")
        logging.info("Map dumped and written to file asynchronously!")

    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)


if __name__ == "__main__":
    run(main())
