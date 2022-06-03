import argparse

from utils import get_galaxy_instance

def get_deversioned_id(tool_id):
    return '/'.join(tool_id.split('/')[:-1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy instance')
    parser.add_argument('-a', '--api_key', help='Galaxy api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles.yml')
    args = parser.parse_args()

    galaxy_instance = get_galaxy_instance(args.galaxy_url, args.api_key, args.profile)
    tools = [get_deversioned_id(t['id']) for t in galaxy_instance.tools.get_tools() if t.get('tool_shed_repository')]
    repos = [(r['name'], r['owner']) for r in galaxy_instance.toolshed.get_repositories() if r['status'] == 'Installed']

    print('Tools in panel: %d' % len(list(set(tools))))
    print('All tools: %d' % len(tools))
    print('Installed repositories by name and owner: %d' % len(list(set(repos))))
    print('All installed repositories: %d' % len(repos))


if __name__ == "__main__":
    main()
