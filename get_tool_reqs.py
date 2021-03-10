import argparse
from utils import get_galaxy_instance, user_is_admin


def main():
    parser = argparse.ArgumentParser(description='Get installed versions and revisions on GA')
    parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy instance')
    parser.add_argument('-a', '--api_key', help='Galaxy admin api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles.yml')
    parser.add_argument('-e', '--env', help='Show env path', action='store_true')
    args = parser.parse_args()

    galaxy_instance = get_galaxy_instance(args.galaxy_url, args.api_key, args.profile)
    if not user_is_admin(galaxy_instance):
        print('Non-admin accounts cannot access this info')
        return

    args = parser.parse_args()
    print(get_requirement_str_for_tool_id(galaxy_instance, args.tool_id, args.env))


def get_requirement_str_for_tool_id(galaxy_instance, tool_id, include_env=False):
    requirements = galaxy_instance.tools.requirements(tool_id)
    if not requirements:
        print('No requirements for %s' % tool_id)
        return
    return_str = ' '.join(['%s=%s' % (r['name'], r['version']) for r in requirements])
    if include_env:
        return_str += f' ({requirements[0].get("environment_path")})'
    return return_str

if __name__ == '__main__':
    main()
