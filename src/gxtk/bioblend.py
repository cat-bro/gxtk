# Simple bioblend calls
import json
import yaml
from .utils import ConfigClient, get_profile_key_or_url
from bioblend import ConnectionError

def decode_id(galaxy_instance, args):
    galaxy_instance.config = ConfigClient(galaxy_instance)
    try:
        print(galaxy_instance.config.decode_id(args.api_id).get('decoded_id'))
    except ConnectionError as e:
        print(e)

def write_tool_list(galaxy_instance, args):
    # dump galaxy_instance.tools.get_tools() to a file
    if args.output_path:
        fname = args.output_path
    else:
        identifier = get_profile_key_or_url(args.galaxy_url, args.api_key, args.profile, args.profiles_path)
        format = 'yml' if args.format == 'yaml' else 'json'
        fname = f'{identifier}.{format}'
    with open(fname, 'w') as handle:
        tool_list = galaxy_instance.tools.get_tools()
        print(f'Writing tool list to {fname}')
        if args.format == 'yaml':
            yaml.safe_dump(tool_list, handle)
        elif args.format == 'json':
            handle.write(json.dumps(tool_list))




