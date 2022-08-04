from .bioblend import decode_id, write_tool_list
from .find_tools import get_tool_details
from .utils import get_galaxy_instance, user_is_admin, show_keys
from .test import run_tool_test
from .delete_histories import delete_histories
from .conda_commands import print_conda_commands
from .mulled_hash import mulled_hash
from .reload_tool import reload_tool

from .requirements import show_requirements, show_env
from .command_line import command_line_parser


def main():
    parser = command_line_parser()
    args = parser.parse_args()

    if args.require_galaxy:
        galaxy_instance = get_galaxy_instance(
            url=args.galaxy_url,
            api_key=args.api_key,
            profile=args.profile,
            profiles_path=args.profiles_path,
        )
 
    if args.require_login:
        if not galaxy_instance.key:
            print(f'Login required for {args.action} command')
            return

    if args.require_admin:
        if not user_is_admin(galaxy_instance):
            print(f'Non-admin accounts cannot perform this command: {args.action}')
            return

    if args.action == 'test':
        run_tool_test(galaxy_instance, args)
        return

    if args.action == 'delete-histories':
        delete_histories(galaxy_instance, args)
        return

    if args.action == 'find':
        get_tool_details(galaxy_instance, args)
        return

    if args.action == 'conda-commands':
        print_conda_commands(galaxy_instance, args)
        return

    if args.action == 'mulled-hash':
        mulled_hash(args)
        return

    if args.action == 'show-keys':
        show_keys(args.profiles_path)
        return

    if args.action == 'decode':
        decode_id(galaxy_instance, args)
        return

    if args.action == 'requirements':
        show_requirements(galaxy_instance, args)
        return

    if args.action == 'env-name':
        show_env(galaxy_instance, args)
        return

    if args.action == 'get-tools':
        write_tool_list(galaxy_instance, args)
        return

    if args.action == 'reload':
        reload_tool(galaxy_instance, args)
        return


if __name__ == "__main__":
    main()
