import argparse
import os

from utils import get_galaxy_instance

default_galaxy_url = 'https://usegalaxy.org.au'


def main():
    parser = argparse.ArgumentParser(description='Get installed versions and revisions on GA')
    parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy instance')
    parser.add_argument('-a', '--api_key', help='Galaxy admin api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles.yml')
    args = parser.parse_args()

    galaxy_instance = get_galaxy_instance(args.galaxy_url, args.api_key, args.profile)

    print(get_mulled_env_for_tool_id(galaxy_instance=galaxy_instance, tool_id=args.tool_id))


def get_mulled_env_for_tool_id(galaxy_instance, tool_id):
    requirements = galaxy_instance.tools.requirements()
    return get_env_from_requirements(requirements)


def get_env_from_requirements(requirements):
    if not requirements:
        return '<No requirements>'
    else:
        environment_path = requirements[0].get('environment_path')
        if not environment_path:
            return '<No env>'
        else:
            return os.path.basename(environment_path)


if __name__ == '__main__':
    main()
