import os


def get_env_from_requirements(requirements, basename=True):
    if not requirements:
        return '<No requirements>'
    else:
        env_path = requirements[0].get('environment_path')
        if not env_path:
            return '<No env>'
        else:
            return os.path.basename(env_path) if basename else env_path


def get_channel_str_from_requirements(requirements):
    channels = requirements[0].get('dependency_resolver').get('ensure_channels').split(',')
    return ' '.join([f'-c {channel}' for channel in channels])


def get_requirement_str_for_tool_id(galaxy_instance, tool_id, include_env=False):
    requirements = galaxy_instance.tools.requirements(tool_id)
    if not requirements:
        print('No requirements for %s' % tool_id)
        return
    return_str = get_req_str_from_requirements(requirements)
    if include_env:
        return_str += get_env_from_requirements(requirements)
    return return_str


def get_req_str_from_requirements(requirements):
    return ' '.join(['%s=%s' % (r['name'], r['version']) for r in requirements])
