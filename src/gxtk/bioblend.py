# Simple bioblend calls
from .utils import ConfigClient

def decode_id(galaxy_instance, args):
    galaxy_instance.config = ConfigClient(galaxy_instance)
    print(galaxy_instance.config.decode_id(args.api_id))