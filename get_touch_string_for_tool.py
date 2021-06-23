import argparse
import os

from utils import get_galaxy_instance, user_is_admin, get_tool_client

"""
Some tools don't run on pulsar because outputs do not exist at the end of a job.  Galaxy
would not care but pulsar fails the job.  This script generates a string of 'touch filename'
commands to create empties of all of the output files.  Put this at the beginning of cdata in
the tool wrapper.  Run reload_tool.py <tool_id> once it has been added.
"""

# note: this is gross but it seems to work

def main():
    parser = argparse.ArgumentParser(description='Reload a tool on Galaxy (admin only)')
    parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy instance')
    parser.add_argument('-a', '--api_key', help='Galaxy admin api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles.yml')
    args = parser.parse_args()

    galaxy_instance = get_galaxy_instance(args.galaxy_url, args.api_key, args.profile)

    details = galaxy_instance.tools.show_tool(args.tool_id, io_details=True)

    gnarly_string = ' '.join(['touch %s &&' % o['from_work_dir'] for o in details['outputs']])

    print(gnarly_string)


if __name__ == '__main__':
    main()

