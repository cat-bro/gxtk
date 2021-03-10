import os
import yaml

from bioblend.galaxy import GalaxyInstance

profiles_path = 'profiles.yml'

def get_galaxy_instance(url, api_key, profile):
    if not url and not profile:
        profile = 'default'
    if profile or not url:
        if os.path.exists(profiles_path):
            with open(profiles_path) as handle:
                profiles = yaml.safe_load(handle)
        else:
            raise Exception('Profiles file %s not found' % profiles_path)
        prof = profiles[profile] if profile else profiles['default']
        url = prof['url']  # must exist
        if not api_key:
            api_key = prof.get('api_key') # can be None
    return GalaxyInstance(url, api_key)
