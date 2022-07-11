import time
import yaml
from pprint import pprint
from tabulate import tabulate
import packaging.version

from .requirements import get_env_from_requirements, get_req_str_from_requirements
from .utils import user_is_admin, indent, reverse_version_order, section_label_order, load_edam_dicts

display_changeset_revision = True

def get_tool_details(galaxy_instance, args):

    name = args.name
    display_name = args.display_name
    version = args.version
    owner = args.owner
    fuzz = args.fuzz
    tool_ids = args.tool_ids
    env = args.env
    biotools = args.biotools
    edam_topics = args.edam_topics
    all = args.all
    latest = args.latest
    labels = args.labels
    output_format = args.output_format
    section_label = args.section_label

    display_edam_topics, edam_filter = optional_column_or_filter(edam_topics)
    display_biotools_ids, biotools_filter = optional_column_or_filter(biotools)
    biotools = biotools_filter is not None
    edam_topics = edam_filter is not None

    tools = galaxy_instance.tools.get_tools()
    if edam_topics:
        labels_from_topic_id, topic_ids_from_label = load_edam_dicts()

    filtering_args = [
        'name', 'owner', 'display_name', 'version',
        'labels', 'all', 'tool_ids', 'biotools', 'edam_topics'
    ]

    if not any([x is not None for x in filtering_args]):
        print(f'At least one of name, {", ".join(filtering_args[:-1])} or {filtering_args[-1]} must be specified')
        return
    if not all and not tool_ids:
        if name and not fuzz:
            tools = [t for t in tools if t.get('tool_shed_repository') and t['tool_shed_repository']['name'] == name]
        if name and fuzz:
            tools = [t for t in tools if t.get('tool_shed_repository') and name in t['tool_shed_repository']['name']]
        if display_name:
            tools = [t for t in tools if display_name.lower() in t['name'].lower()]
        if version:
            tools = [t for t in tools if version in t['version']]
        if section_label:
            tools = [t for t in tools if t['panel_section_name'] is not None and section_label.lower() == t['panel_section_name'].lower()]
        if owner:
            tools = [t for t in tools if t.get('tool_shed_repository') and t['tool_shed_repository']['owner'] in owner]
        if labels:
            tools = [t for t in tools if any([label in t.get('labels') for label in labels])]
        if edam_filter:
            tools = [t for t in tools if edam_filter(
                [labels_from_topic_id[et] for et in t.get('edam_topics')]
            )]
        if biotools_filter:
            tools = [t for t in tools if biotools_filter(get_biotools_ids(t))]
    elif tool_ids:
        tools = [t for t in tools if t['id'] in tool_ids]
    if latest and not version and not tool_ids:
        tools = filter_for_latest_versions(tools)
    if not tools:
        print('No tools found')
        return

    # Section label followed by deversioned tool id followed by version newest first
    tools = sorted(tools, key=lambda x: (
        section_label_order(x['panel_section_name']),
        get_deversioned_id(x['id']),
        reverse_version_order(x['version']),
    ))

    table_def = [
        {
            'header': 'Display Name',
            'get_value': lambda x: x.get('name'),
            'show_value': True
        },
        {
            'header': 'Repo Name',
            'get_value': lambda x: x.get('tool_shed_repository', {}).get('name', '-'),
            'show_value': True,
        },
        {
            'header': 'Owner',
            'get_value': lambda x: x.get('tool_shed_repository', {}).get('owner', '-'),
            'show_value': True,
        },
        {
            'header': 'Revision',
            'get_value': lambda x: x.get('tool_shed_repository', {}).get('changeset_revision', '-'),
            'show_value': display_changeset_revision,
        },
        {
            'header': 'Version',
            'get_value': lambda x: x.get('version'),
            'show_value': True,
        },
        {
            'header': 'Edam Topics',
            'get_value': (
                lambda x: ','.join([
                    labels_from_topic_id.get(topic) for topic in x.get('edam_topics')
                    ] if x.get('edam_topics') else '-')
                ),
            'show_value': display_edam_topics,
        },
        {
            'header': 'Bio.tools ID',
            'get_value': get_biotools_display,
            'show_value': display_biotools_ids,
        },
        {
            'header': 'Section Label',
            'get_value': lambda x: x.get('panel_section_name'),
            'show_value': True,
        },
        {
            'header': 'Tool ID',
            'get_value': lambda x: x.get('id'),
            'show_value': True,
        },
        {
            'header': 'Environment',
            'get_value': lambda x: get_env_from_requirements(galaxy_instance.tools.requirements(x['id'])),
            'show_value': env and user_is_admin(galaxy_instance),
        },
    ]

    if output_format in ['plain', 'tsv']:
        header = [c['header'] for c in table_def if c['show_value']]
        def get_row(tool):
            return [c['get_value'](tool) for c in table_def if c['show_value']]

        rows = [get_row(tool) for tool in tools]
    
        if output_format == 'tsv':
            print('\t'.join(header))
            for row in rows:
                print('\t'.join([str(r) for r in row]))
        
        else:
             print(tabulate(rows, headers=header, tablefmt='plain'))
    elif output_format == 'shed-tools':
        output_shed_tools(tools)
    elif output_format == 'miniconda':
        if user_is_admin(galaxy_instance):
            output_for_miniconda(galaxy_instance, tools)
        else:
            print('miniconda output requires an admin api key')
    elif output_format == 'ids':
        print('\n'.join([t['id'] for t in tools]))
    else:
        print(f'Unrecognised output format {output_format}: options are plain, tsv, shed-tools or ids')


def get_deversioned_id(tool_id):
    if '/' in tool_id:
        return '/'.join(tool_id.split('/')[:-1])
    else:
        return tool_id

def sort_by_version(tool_list):
    return sorted(tool_list, key=lambda x: packaging.version.parse(x['version']), reverse=True)

def filter_for_latest_versions(tool_list):
    latest_list = []
    processed_ids = []
    for tool in tool_list:
        if tool['id'] in processed_ids:
            continue
        same_tools = [t for t in tool_list if get_deversioned_id(t['id']) == get_deversioned_id(tool['id'])]
        latest_tool = sort_by_version(same_tools)[0]
        latest_list.append(latest_tool)
        processed_ids.extend([t['id'] for t in same_tools])
    return latest_list

def output_shed_tools(tools):
    shed_tools = []
    for tool in tools:
        if not tool.get('tool_shed_repository'):
            continue
        tsr = tool['tool_shed_repository']
        if [st for st in shed_tools if (
            st['name'] == tsr['name'] and
            st['owner'] == tsr['owner'] and
            st['revisions'][0] == tsr['changeset_revision']            
        )]:
            continue # skip because it is already in the list
        shed_tools.append({
            'name': tsr['name'],
            'owner': tsr['owner'],
            'tool_panel_section_label': tool['panel_section_name'] or 'None',
            'revisions': [tsr['changeset_revision']],
            'tool_shed_url': tsr['tool_shed'],
        })
    print(yaml.dump({'tools': shed_tools}))

def output_for_miniconda(galaxy_instance, tools):
    envs = {}
    for tool in tools:
        requirements = galaxy_instance.tools.requirements(tool['id'])
        pprint(requirements)
        env_name = get_env_from_requirements(requirements)
        if env_name == '<No env>':
            print(f'Warning: Tool with ID {tool["id"]} does not have a resolved conda environment.  Skipping')
            continue
        if env_name in envs:
            continue
        req_str = get_req_str_from_requirements(requirements)
        envs[env_name] = {}
        envs[env_name]['packages'] = req_str.split(' ')
    print(yaml.dump({'miniconda_conda_environments': envs}))

def optional_column_or_filter(filter_list):  # TODO: filter for empty, filter for any
    display = False
    filter = None # no filter
    if not filter_list:
        display = True
    elif filter_list == ['DO_NOT_DISPLAY']:
        pass # default
    elif filter_list == ['any']:
        display = True
        filter = lambda x: len(x) > 0
    else:
        display = True
        filter = lambda x: any([y in x for y in filter_list])
    return (display, filter)

def get_biotools_display(tool):
    biotools_ids = get_biotools_ids(tool)
    return ', '.join(biotools_ids) if biotools_ids else '-'

def get_biotools_ids(tool):
    return [r['value'] for r in tool.get('xrefs') if r['reftype'] == 'bio.tools']
