# Simple bioblend calls
from .utils import ConfigClient
from bioblend import ConnectionError

def decode_id(galaxy_instance, args):
    galaxy_instance.config = ConfigClient(galaxy_instance)
    try:
        print(galaxy_instance.config.decode_id(args.api_id).get('decoded_id'))
    except ConnectionError as e:
        print(e)