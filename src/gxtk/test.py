import datetime as dt
import urllib
import yaml
import os

from .utils import get_profile_key_or_url, get_test_dir, get_test_history_file

from galaxy.tool_util.verify.script import build_case_references, test_tools, Results, setup_global_logger
from galaxy.tool_util.verify.interactor import GalaxyInteractorApi

datetime_local = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
datetime_utc = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

test_history_file = get_test_history_file

def get_history(self, history_name="test_history"):
    # Return the most recent non-deleted history matching the provided name
    filters = urllib.parse.urlencode({'q': 'name', 'qv': history_name, 'order': 'update_time'})
    response = self._get(f"histories?{filters}")
    try:
        return response.json()[-1]
    except IndexError:
        return None

GalaxyInteractorApi.get_history = get_history

def get_json_filename(tool_id, tags, profile_id, results_dir):
    test_dir = get_test_dir()
    if not os.path.exists(os.path.join(test_dir, profile_id)):
        os.mkdir(os.path.join(test_dir, profile_id))
    # TODO: path needs to be built from results_dir and profile_key if results_dir is set
    short_name = ('_'.join(tool_id.split('/')[-2:])).replace('.*', 'latest') if '/' in tool_id else tool_id
    basename = short_name
    if tags:
        basename += f'_{"_".join(sorted(tags))}'
    basename += '.test.json'
    if test_dir:
        return os.path.join(test_dir, profile_id, basename)
    else:
        return basename  # TODO: allow user to provide output filename


def get_version_from_id(tool_id):
    if '/' in tool_id:
        version = tool_id.split('/')[-1]
        if not version == '.*':
            return version

def get_deversioned_id(tool_id):  # TODO: move to utils
    if '/' in tool_id:
        return '/'.join(tool_id.split('/')[:-1])
    else:
        return tool_id

def run_tool_test(galaxy_instance, args):
    tool_id = args.tool_id
    tags = args.tags
    results_dir = args.results_dir
    profile_id = get_profile_key_or_url(args.galaxy_url, args.api_key, args.profile, args.profiles_path)
    galaxy_url = galaxy_instance.url.replace('api', '')
    test_history_name = f'Test history for {tool_id} {datetime_utc}'
    history = galaxy_instance.histories.create_history(name=test_history_name)
    if tags:
        galaxy_instance.histories.update_history(history['id'], tags=tags)

    interactor = GalaxyInteractorApi(
        galaxy_url=galaxy_url,
        master_api_key=galaxy_instance.key,
        api_key=galaxy_instance.key, 
        keep_outputs_dir='',
        test_data=args.test_data or [],
    )

    references = build_case_references(galaxy_interactor=interactor, tool_id=get_deversioned_id(tool_id), tool_version=get_version_from_id(tool_id))

    results = Results(
        f'Test of {tool_id}',
        get_json_filename(tool_id, tags, profile_id, results_dir),
        append=False,  # append=True could be a good thing
        galaxy_url=galaxy_url,
    )
    verify_kwds = {'skip_with_reference_data': True}
    test_tools(galaxy_interactor=interactor, test_references=references, results=results,
        history_name=test_history_name, no_history_reuse=False, log=setup_global_logger(__name__, verbose=False),
        verify_kwds=verify_kwds, parallel_tests=args.parallel_tests)
