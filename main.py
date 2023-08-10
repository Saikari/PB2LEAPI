import logging
from asyncio import run

from DataInterfaces.MapIO import MapIO
from Utils.mapTools import MapTools

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize map tools
mapTools = MapTools()


# Example usage
async def main():
    try:
        map_data = mapTools.getMapByIdOnline('sgt dwayne-sentry', xml=True)
        map_instance = await MapIO.load_map_from_object_async(map_data)
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
