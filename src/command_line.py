import argparse

def common_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy instance')
    parser.add_argument('-a', '--api_key', help='Galaxy api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles.yml')
    return parser

def command_line_parser():
    command_line_common = common_args()
    command_parser = argparse.ArgumentParser()
    subparsers = command_parser.add_subparsers()

    find_parser = subparsers.add_parser(
        'find',
        help='', # TODO: add help
        parents=[command_line_common],
    )

    delete_histories_parser = subparsers.add_parser(
        'delete-histories',
        help='', # TODO: add help
        parents=[command_line_common],
    )

    test_parser = subparsers.add_parser(
        'test',
        help='', # TODO: add help
        parents=[command_line_common],
    )

    conda_commands_parser = subparsers.add_parser(
        'conda-commands',
        help='', # TODO: add help
        parents=[command_line_common],
    )

    reload_parser = subparsers.add_parser(
        'reload',
        help='', # TODO: add help
        parents=[command_line_common],
    )
    reload_parser.set_defaults(action='reload', require_galaxy=True, require_login=True, require_admin=True)

    mulled_hash_parser = subparsers.add_parser(
        'mulled-hash',
        help='', # TODO: add help
        parents=[],
    )
    mulled_hash_parser.set_defaults(action='mulled-hash', require_galaxy=False, require_login=False, require_admin=False)

    find_parser.set_defaults(action='find', require_galaxy=True, require_login=False, require_admin=False)
    delete_histories_parser.set_defaults(action='delete-histories', require_galaxy=True, require_login=True, require_admin=False)
    test_parser.set_defaults(action='test', require_galaxy=True, require_login=True, require_admin=False)
    conda_commands_parser.set_defaults(action='conda-commands', require_galaxy=True, require_login=True, require_admin=True)

    for parser in [find_parser]:
        parser.add_argument('-n', '--name', help='Tool repository name')
        parser.add_argument('-N', '--display_name', help='User facing tool name')
        parser.add_argument('-v', '--version', help='Version')
        parser.add_argument('-o', '--owner', nargs='+', help='Show tools from one or more owners')
        parser.add_argument('-z', '--fuzz', action='store_true', help='Match substring of repository name from search term')
        parser.add_argument('--all', help='Show all installed tools', action='store_true')
        parser.add_argument('-e', '--env', help='Show virtual environment name (admin API key required)', action='store_true')
        parser.add_argument('-b', '--biotools', help='Show bio.tools IDs in output', action='store_true')  
        parser.add_argument('-t', '--tool_ids', nargs='+', help='One or more tool ids to match exactly')
        parser.add_argument('-s', '--sleep', action='store_true', help='Sleep for 0.5s after fetching requirements') # TODO: get rid of this

    for parser in [test_parser]:
        parser.add_argument('-t', '--tool_ids', nargs='+', help='One or more tool ids to match exactly')
        parser.add_argument('--tags', nargs='+', help='Tags for test history')

    for parser in [delete_histories_parser]:
        parser.add_argument('--name_startswith', help='History name prefix')
        parser.add_argument('--days_since_updated', type=int, help='Last updated more than X days ago')
        parser.add_argument('--delete_all', action='store_true', help='In the absence of conditions include this argument to delete all histories')
        parser.add_argument('--skip_wait', action='store_true', help='Do not wait while large histories are deleted, allow them to delete in the background')
        parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation step prior to deleting histories')

    for parser in [conda_commands_parser]:
        parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)
        parser.add_argument('-m', '--mamba', action='store_true', help='Use mamba instead of conda in install command')

    for parser in [reload_parser]:
        parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)

    for parser in [mulled_hash_parser]:
        parser.add_argument('requirements', help='One or more conda requirements e.g. balloon=1.1 or fish=3.2b', nargs='+')


    return command_parser