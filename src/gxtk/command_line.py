import argparse

def common_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy instance')
    parser.add_argument('-a', '--api_key', help='Galaxy api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles yaml file')
    parser.add_argument('--profiles_path', help='Path to profiles yaml file (default ~/.gxtk.yml)')
    return parser

def command_line_parser():
    command_line_common = common_args()
    command_parser = argparse.ArgumentParser()
    subparsers = command_parser.add_subparsers()

    find_parser = subparsers.add_parser(
        'find',
        help="Filter tool list for a galaxy instance by properties including repository name, display name "
        "and owner.  Default output is a tab separated table of tools.  Optional return fields include "
        "bio.tools ID.  Admin users can include the tool's conda environment name (-e flag) in output.",
        # TODO: add help
        parents=[command_line_common],
    )

    reload_parser = subparsers.add_parser(
        'reload',
        help="Reload tool in panel", # TODO: add help
        parents=[command_line_common],
    )
    reload_parser.set_defaults(action='reload', require_galaxy=True, require_login=True, require_admin=True)

    requirements_parser = subparsers.add_parser(
        'requirements',
        help="Print conda package requirements for tool ID (admin only).", # TODO: add help
        parents=[command_line_common],
    )
    requirements_parser.set_defaults(action='requirements', require_galaxy=True, require_login=True, require_admin=True)

    env_name_parser = subparsers.add_parser(
        'env-name',
        help="Print conda environment name for tool ID (admin only).", # TODO: add help
        parents=[command_line_common],
    )
    env_name_parser.set_defaults(action='env-name', require_galaxy=True, require_login=True, require_admin=True)


    conda_commands_parser = subparsers.add_parser(
        'conda-commands',
        help="Print out conda command for uninstalling and reinstalling an environment from "
            "<conda dir>/envs directory where the conda base enviroment is active. "
            "The purpose is for reinstalling environments where the environment has errors.",
        parents=[command_line_common],
    )

    mulled_hash_parser = subparsers.add_parser(
        'mulled-hash',
        help="Generate a galaxy conda mulled hash (v1) from a list of requirements", # TODO: add help
        parents=[],
    )
    mulled_hash_parser.set_defaults(action='mulled-hash', require_galaxy=False, require_login=False, require_admin=False)


    delete_histories_parser = subparsers.add_parser(
        'delete-histories',
        help="""
Delete histories belonging to user.  This will wait for small histories that can be deleted within 2-3 minutes.
For histories that take longer than nginx takes to time out, the script waits until the history has state 'deleted'
unless the --skip_wait flag is included in the command.
""",
        parents=[command_line_common],
    )

    test_parser = subparsers.add_parser(
        'test',
        help="Wrapper for galaxy-tool-util's galaxy-tool-test.", # TODO: add help
        parents=[command_line_common],
    )

    get_tools_parser = subparsers.add_parser(
        # TODO: deprecate this in favour of built-in saving through `gxtk find`
        'get-tools',
        help="Save tool list to a JSON or yaml file.",
        parents=[command_line_common],
    )
    get_tools_parser.set_defaults(action='get-tools', require_galaxy=True, require_login=False, require_admin=False)

    decode_parser = subparsers.add_parser(
        'decode',
        help="Translate API ID to integer database ID (admin only).", # TODO: add help
        parents=[command_line_common],
    )
    decode_parser.set_defaults(action='decode', require_galaxy=True, require_login=True, require_admin=True)

    show_keys_parser = subparsers.add_parser(
        'show-keys',
        help="List keys in profiles file (~/.gxtk.yml by default)", # TODO: add help
        parents=[command_line_common],
    )
    show_keys_parser.set_defaults(action='show-keys', require_galaxy=False, require_login=False, require_admin=False)

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
        parser.add_argument('-t', '--tool_ids', nargs='+', help='One or more tool ids to match exactly')
        parser.add_argument('-V', '--all_versions', action='store_true', help='Search from complete list of tools including older versions')
        parser.add_argument('-s', '--section_label', help='Tool Section label')
        parser.add_argument('--all_tools', help='Show all installed tools', action='store_true')
        parser.add_argument('--labels', nargs='+', help='Tool label')
        parser.add_argument('--biotools', nargs='*', help='Enter flag to show bio.tools IDs in output, add arguments to filter by bio.tool IDs', default=['DO_NOT_DISPLAY']) 
        parser.add_argument('--edam_topics', nargs='*', help='Enter flag to show Edam topics in output, add arguments to filter by topics',  default=['DO_NOT_DISPLAY'])
        parser.add_argument('-e', '--env', help='Show virtual environment name (admin API key required)', action='store_true')
        parser.add_argument('-f', '--output-format', help='Format of output list plain(default)|tsv', default='plain')
        parser.add_argument('-S', '--source', help='Path to a json file containing tool list')

    for parser in [delete_histories_parser]:
        parser.add_argument('--name_startswith', help='History name prefix')
        parser.add_argument('--days_since_updated', type=int, help='Last updated more than X days ago')
        parser.add_argument('--delete_all', action='store_true', help='In the absence of conditions include this argument to delete all histories')
        parser.add_argument('--skip_wait', action='store_true', help='Do not wait while large histories are deleted, allow them to delete in the background')
        parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation step prior to deleting histories')
        parser.add_argument('--user_email', help='Email address of user account. This provides an optional extra integrity check that the API key provided was for the intended user')

    for parser in [conda_commands_parser, env_name_parser, requirements_parser, test_parser]:
        parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)

    for parser in [conda_commands_parser]:
        parser.add_argument('-m', '--mamba', action='store_true', help='Use mamba instead of conda in install command')

    for parser in [test_parser]:
        # parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)  # TODO: other ways to specify tool
        parser.add_argument('--tags', nargs='+', help='Tags for test history')
        parser.add_argument('--results_dir', help='base directory for tool test results (defaults to $GXTK_RESULTS_DIR)')
        parser.add_argument('--test_data', nargs='+', help='Local test data paths')  # TODO: add command line options from galaxy-tool-test
        parser.add_argument('-P', '--parallel_tests', type=int, default=1, help='Number of tests to run in parallel')  # TODO: add command line options from galaxy-tool-test

    for parser in [reload_parser]:
        parser.add_argument('-t', '--tool_id', help='Tool ID', required=True)

    for parser in [mulled_hash_parser]:
        parser.add_argument('requirements', help='One or more conda requirements e.g. balloon=1.1 or fish=3.2b', nargs='+')

    for parser in [decode_parser]:
        parser.add_argument('api_id', help='Encoded hexadecimal object ID')

    for parser in [get_tools_parser]:
        parser.add_argument('-o', '--output_path', help='Output file name')
        parser.add_argument('-f', '--format', help='Format (yaml or json, default json)', default='json')


    return command_parser