import argparse

from bioblend.galaxy import GalaxyInstance

from get_tool_env import get_env_from_requirements
from utils import get_galaxy_instance


def main():
    parser = argparse.ArgumentParser(description='Get installed versions and revisions on GA')
    parser.add_argument('-n', '--name', help='Tool name')
    parser.add_argument('-N', '--display_name', help='User facing tool name')
    parser.add_argument('-v', '--version', help='Version')
    parser.add_argument('-z', '--fuzz', action='store_true', help='Match name including string')
    parser.add_argument('--all', help='Show all installed tools', action='store_true')
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy instance')
    parser.add_argument('-a', '--api_key', help='Galaxy admin api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles.yml')

    args = parser.parse_args()
    name = args.name
    display_name = args.display_name
    version = args.version
    fuzz = args.fuzz
    all = args.all

    galaxy_instance = get_galaxy_instance(args.galaxy_url, args.api_key, args.profile)
    is_admin = galaxy_instance.config.get_config().get('is_admin_user', False)
    tools = [t for t in galaxy_instance.tools.get_tools() if t.get('tool_shed_repository')]

    if not all:
        if not (name or display_name):
            print('either name or display_name must be specified')
            return
        if name and not fuzz:
            tools = [t for t in tools if t['tool_shed_repository']['name'] == name]
        if name and fuzz:
            tools = [t for t in tools if name in t['tool_shed_repository']['name']]
        if display_name:
            tools = [t for t in tools if display_name.lower() in t['name'].lower()]
        if version:
            tools = [t for t in tools if version in t['version']]
    if not tools:
        print('No tools found')
        return
    include_env = is_admin  # might refine logic around including env by default for admins

    def get_row(tool):
        row = [
            tool['name'],
            tool['tool_shed_repository']['name'],
            tool['tool_shed_repository']['owner'],
            tool['tool_shed_repository']['changeset_revision'],
            tool['version'],
            tool['panel_section_name'],
            tool['id'],
        ]
        if include_env:
            row.append(get_env_from_requirements(galaxy_instance.tools.requirements(tool['id'])) or '-')
        return row
    
    header = ['Display Name', 'Repo name', 'Owner', 'Revision', 'Version', 'Section Label', 'Tool ID']
    if include_env:
        header.append('Environment')
    rows = [get_row(tool) for tool in tools]
 
    print('\t'.join(header))
    for row in rows:
        print('\t'.join(row))


if __name__ == "__main__":
    main()
