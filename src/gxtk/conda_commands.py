from .requirements import get_channel_str_from_requirements, get_env_from_requirements, get_req_str_from_requirements

flags = ['--quiet', '--override-channels']

"""
This script prints out conda commands for uninstalling and reinstalling an environment from
_conda/envs directory where the conda base enviroment is active.  The purpose is for reinstalling environments where
the environment has errors.
"""

def get_channel_str_from_requirements(requirements):
    channels = requirements[0].get('dependency_resolver').get('ensure_channels').split(',')
    return ' '.join([f'-c {channel}' for channel in channels])

def print_conda_commands(galaxy_instance, args):
    requirements = galaxy_instance.tools.requirements(args.tool_id)
    if not requirements:
        print(f'No requirements for tool {args.tool_id}')
        return
    req_str = get_req_str_from_requirements(requirements)
    channel_str = get_channel_str_from_requirements(requirements)
    env_name = get_env_from_requirements(requirements)
    resolver = 'mamba' if args.mamba else 'conda'
    print(f'# {env_name} ({args.tool_id})')
    print(f'conda env remove -n {env_name}')
    print(f'conda create -y --prefix {env_name}')
    print(f'{resolver} install -y -n {env_name} {" ".join(flags)} {channel_str} {req_str}')
