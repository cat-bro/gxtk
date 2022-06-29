import datetime as dt
import urllib

from galaxy.tool_util.verify.script import build_case_references, test_tools, Results, setup_global_logger
from galaxy.tool_util.verify.interactor import GalaxyInteractorApi

def get_history(self, history_name="test_history"):
    # Return the most recent non-deleted history matching the provided name
    filters = urllib.parse.urlencode({'q': 'name', 'qv': history_name, 'order': 'update_time'})
    response = self._get(f"histories?{filters}")
    try:
        return response.json()[-1]
    except IndexError:
        return None

GalaxyInteractorApi.get_history = get_history

def get_version_from_id(tool_id):
    if '/' in tool_id:
        return '/'.split(tool_id)[-1]

def run_tool_test(galaxy_instance, tool_id, tags=[]):
    galaxy_url = galaxy_instance.url.replace('api', '')
    test_history_name = f'Test history for {tool_id} {dt.datetime.now().strftime("%Y/%m/%d %H/%M/%S")}'
    history = galaxy_instance.histories.create_history(name=test_history_name)
    if tags:
        galaxy_instance.histories.update_history(history['id'], tags=tags)

    interactor = GalaxyInteractorApi(
        galaxy_url=galaxy_url,
        master_api_key=galaxy_instance.key,
        api_key=galaxy_instance.key, 
        keep_outputs_dir='',
    )

    references = build_case_references(galaxy_interactor=interactor, tool_id=tool_id, tool_version=get_version_from_id(tool_id))
    results = Results(f'Test of {tool_id}', '/Users/cat/dev/gxtk/test_pip/test', append=False, galaxy_url=galaxy_url)
    verify_kwds = {'skip_with_reference_data': True}
    test_tools(galaxy_interactor=interactor, test_references=references, results=results,
        history_name=test_history_name, no_history_reuse=False, log=setup_global_logger(__name__, verbose=False),
        verify_kwds=verify_kwds)
