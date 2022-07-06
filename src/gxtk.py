from .functions.find_tools import get_tool_details
from .functions.utils import get_galaxy_instance, user_is_admin, show_keys
from .functions.test import run_tool_test
from .functions.delete_histories import delete_histories
from .functions.conda_commands import print_conda_commands
from .functions.mulled_hash import mulled_hash

from .functions.requirements import get_requirement_str_for_tool_id

from .functions.command_line import command_line_parser


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

    # if args.action == 'show-requirements':
    #     print(get_requirement_str_for_tool_id(galaxy_instance, args.tool_ids[0], False))
    #     return

    if args.action == 'test':
        run_tool_test(galaxy_instance, args.tool_ids[0], tags=args.tags)
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


if __name__ == "__main__":
    main()
