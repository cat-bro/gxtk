from argparse import Action
import os
import yaml

from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.tools import ToolClient as bioblend_ToolClient
from bioblend.galaxy.config import ConfigClient as bioblend_ConfigClient

from galaxy.tool_util.edam_util import load_edam_tree

# default_profiles_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'profiles.yml')
default_profiles_path = os.path.expanduser('~/.gxtk.yml')
profiles_file_path = os.getenv('GXTK_PROFILES_PATH', default_profiles_path)

link_to_sample_file = '' # TODO: Commit things and fill this in.
check_profiles_example_message = 'See {link_to_sample_file} for an example of the expected format.'

def get_galaxy_instance(url, api_key, profile, profiles_path=profiles_file_path):
    # If the galaxy_url is not provided, the profiles file must exist.
    if profile or not url:
        profiles = get_profiles(profiles_path)
        profile_key = profile or profiles.get('default', profiles.get('__default'))
        if not isinstance(profile_key, str):
            raise Exception('Profile key default or __default must be have a string value.')
        prof = profiles.get(profile_key)
        if not prof:
            message = ''
            if profile and not profiles.get(profile):
                message = f'Specified profile {profile} not found in {get_profiles_path(profiles_path)}.'
            if not profiles.get('default', profiles.get('__default')):
                message = f'Profiles path must contain `default` or `__default` key'
            raise Exception(message)

        url = prof['url']  # must exist # TODO try catch gracefully here
        if not api_key:
            api_key = prof.get('api_key', prof.get('key')) # can be None
    return GalaxyInstance(url, api_key)


def user_is_admin(galaxy_instance):
    return galaxy_instance.config.get_config().get('is_admin_user', False)


def get_profiles_path(profiles_path):
    return profiles_path or profiles_file_path


def get_profiles(profiles_path):
    profiles_path = get_profiles_path(profiles_path)
    if os.path.exists(profiles_path):
        with open(profiles_path) as handle:
            profiles = yaml.safe_load(handle)
    else:
        raise Exception(f'Profiles file {profiles_path} not found')
    return profiles   


def get_profile_key_or_url(url, api_key, profile, profiles_path):
    profiles_path = get_profiles_path(profiles_path)
    if profile:
        return profile
    elif url:
        return url
    else:
        profiles = get_profiles(profiles_path)
        return profiles.get('default', profiles.get('__default'))


def show_keys(profiles_path):
    profiles_path = get_profiles_path(profiles_path)  # TODO: fix overwriting argument variable
    profiles = get_profiles(profiles_path)
    default_profile = profiles.get('default', profiles.get('__default'))
    profile_keys = [f'{default_profile} (default)'] + [
        k for k in profiles.keys() if not k in ['default', '__default', default_profile]
    ]
    print('\n'.join(profile_keys))


def fix_url(url, prefix='https://', short=True):
    if short and url.startswith(prefix):
        return url[len(prefix):].strip('/')
    if not short and not url.startswith(prefix):
        return prefix + url
    return url


class ToolClient(bioblend_ToolClient):
    def reload(self, tool_id):  # TODO: this is in bioblend 0.16.0 and can be removed here
        url = self._make_url(tool_id) + '/reload'
        return self._get(url=url)


class ConfigClient(bioblend_ConfigClient):
    def whoami(self):
        url = self._make_url().replace('configuration', 'whoami')  # TODO: this is in bioblend 0.17.0 and can be removed here
        return self._get(url=url)

    def decode_id(self, object_id):  # TODO: add to bioblend
        url = self._make_url(object_id).replace('/configuration', '/configuration/decode')
        return self._get(url=url)

def get_tool_client(galaxy_instance):
    return ToolClient(galaxy_instance)


def get_config_client(galaxy_instance):
    return ConfigClient(galaxy_instance)


def indent(text, spaces):
    lines = text.strip('\n').split('\n')
    res = ''
    indentation = ' ' * spaces
    for line in lines:
        res += f'{indentation}{line}\n'
    return res

class reversor:  # stackoverflow, add ref
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __lt__(self, other):
           return other.obj < self.obj

class reverse_version_order(reversor):
    def __lt__(self, other):
           return (other.obj is None and self.obj is not None) or other.obj < self.obj

class section_label_order(reversor): # TODO: fix this hack
    def __lt__(self, other):
           return other.obj > self.obj if not None in (self.obj, other.obj) else other.obj is None


def get_panel_tools(galaxy_instance):
    # get tool elements from /api/tools?in_panel=True
    tools = []
    panel = galaxy_instance.tools.get_tool_panel()
    for x in panel:
        if x['model_class'] == 'ToolSection':
            tools.extend(x['elems'])
    return tools


def load_edam_topics():  # TODO: return operations
    edam = load_edam_tree()
    labels_from_topic_id = {}
    for key in edam:
        if key.startswith('topic'):
            label = edam[key].get('label')
            labels_from_topic_id[key] = label
    return labels_from_topic_id


class GxtkModule():
    def __init__(self, action=None, require_galaxy=False, require_login=False, require_admin=False):
        self.action = action
        self.require_galaxy = require_galaxy
        self.require_login = require_login
        self.require_admin = require_admin

    def get_galaxy_instance(self, args):
        if not self.require_galaxy:
            return None
        

    def validate_login_level(self, galaxy_instance):
        if self.require_login:
            if not galaxy_instance.key:
                print(f'Login required for {self.action} command')
                return False

        if self.require_admin:
            if not user_is_admin(galaxy_instance):
                print(f'Non-admin accounts cannot access this subcommand: {self.action}')
                return

    def run():
        pass