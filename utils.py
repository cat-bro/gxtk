import os
import yaml

from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.tools import ToolClient as bioblend_ToolClient

#profiles_path = 'profiles.yml'
profiles_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'profiles.yml')

def get_galaxy_instance(url, api_key, profile):
    # If the galaxy_url is not provided, the profiles file must exist.
    if not url and not profile:
        profile = 'default'
    if profile or not url:
        if os.path.exists(profiles_path):
            with open(profiles_path) as handle:
                profiles = yaml.safe_load(handle)
        else:
            raise Exception('Profiles file %s not found:' % profiles_path)
        prof = profiles[profile] if profile else profiles['default']
        url = prof['url']  # must exist
        if not api_key:
            api_key = prof.get('api_key') # can be None
    return GalaxyInstance(url, api_key)


def user_is_admin(galaxy_instance):
    return galaxy_instance.config.get_config().get('is_admin_user', False)


def fix_url(url, prefix='https://', short=True):
    if short and url.startswith(prefix):
        return url[len(prefix):].strip('/')
    if not short and not url.startswith(prefix):
        return prefix + url
    return url


class ToolClient(bioblend_ToolClient):
    def reload(self, tool_id):
        url = self._make_url(tool_id) + '/reload'
        return self._get(url=url)


def get_tool_client(galaxy_instance):
    return ToolClient(galaxy_instance)