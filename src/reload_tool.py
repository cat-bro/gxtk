import argparse
import os

from utils import get_galaxy_instance, user_is_admin, get_tool_client

"""
Reload a tool without having to restart Galaxy.  This requires an admin API key.
"""

def main():
    parser = argparse.ArgumentParser(description='Reload a tool on Galaxy (admin only)')
    parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy instance')
    parser.add_argument('-a', '--api_key', help='Galaxy admin api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles.yml')
    args = parser.parse_args()

    galaxy_instance = get_galaxy_instance(args.galaxy_url, args.api_key, args.profile)
    if not user_is_admin(galaxy_instance):
        print('Non-admin accounts cannot access this api endpoint')
        return

    tool_client = get_tool_client(galaxy_instance)

    tool_client.reload(args.tool_id)

if __name__ == '__main__':
    main()