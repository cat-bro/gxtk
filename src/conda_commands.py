import argparse
import os

from .get_tool_reqs import get_req_str_from_requirements
from .get_tool_env import get_env_from_requirements
from .utils import get_galaxy_instance, user_is_admin

flags = ['--quiet', '--override-channels']
flag_str = ' '.join(flags)
# channels = ['conda-forge', 'bioconda', 'defaults']
# channel_str = ' '.join([f'-c {channel}' for channel in channels])

"""
This script prints out conda commands for uninstalling and reinstalling an environment from
_conda/envs directory where the conda base enviroment is active.  The purpose is for reinstalling environments where
the environment has errors.
"""

def main():
    parser = argparse.ArgumentParser(description='Get specific conda commands for uninstalling and reinstalling a virtual environment on Galaxy (admins only)')
    parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy')
    parser.add_argument('-a', '--api_key', help='Galaxy admin api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles.yml')
    parser.add_argument('-m', '--mamba', action='store_true', help='Use mamba instead of conda in install command')

    args = parser.parse_args()
    galaxy_instance = get_galaxy_instance(args.galaxy_url, args.api_key, args.profile)
    if not user_is_admin(galaxy_instance):
        print('Non-admin accounts cannot access this info')
        return

    print_conda_commands(galaxy_instance, args.tool_id)

def get_channel_str_from_requirements(requirements):
    channels = requirements[0].get('dependency_resolver').get('ensure_channels').split(',')
    return ' '.join([f'-c {channel}' for channel in channels])

def print_conda_commands(galaxy_instance, args):
    requirements = galaxy_instance.tools.requirements(args.tool_id)
    if not requirements:
        print(f'No requirements for tool {args.tool_id}')
        return
    req_str = get_req_str_from_requirements(requirements)
    channel_str = get_channel_str_from_requirements(requirements)
    env_name = get_env_from_requirements(requirements)
    resolver = 'mamba' if args.mamba else 'conda'
    print(f'# {env_name} ({args.tool_id})')
    print(f'conda env remove -n {env_name}')
    print(f'conda create -y --prefix {env_name}')
    print(f'{resolver} install -y -n {env_name} {flag_str} {channel_str} {req_str}')

if __name__ == "__main__":
    main()