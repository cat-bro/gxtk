import argparse
import os

from utils import get_galaxy_instance

channels = ['iuc', 'conda-forge', 'bioconda', 'defaults']
channel_str = ' '.join([f'-c {channel}' for channel in channels])

def main():
    parser = argparse.ArgumentParser(description='Get installed versions and revisions on GA')
    parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy')
    parser.add_argument('-a', '--api_key', help='Galaxy admin api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles.yml')

    args = parser.parse_args()
    galaxy_instance = get_galaxy_instance(args.galaxy_url, args.api_key, args.profile)
    print_conda_commands(galaxy_instance, args.tool_id)


def print_conda_commands(galaxy_instance, tool_id):
    requirements = galaxy_instance.tools.requirements(tool_id)
    req_tuples = [(r['name'], r['version']) for r in requirements]
    req_str = ' '.join([f'{a}={b}' for (a, b) in req_tuples])
    env_name = os.path.basename(requirements[0]['environment_path'])
    print(f'# {env_name} add *****')
    print(f'conda env remove -n {env_name}')
    print(f'conda create -y --prefix {env_name}')
    print(f'conda install -y -n {env_name} {channel_str} {req_str}')

if __name__ == "__main__":
    main()