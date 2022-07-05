import time
from .requirements import get_env_from_requirements
from .utils import user_is_admin

def get_tool_details(galaxy_instance, args):

    name = args.name
    display_name = args.display_name
    version = args.version
    owner = args.owner
    fuzz = args.fuzz
    tool_ids = args.tool_ids
    env = args.env
    biotools = args.biotools
    all = args.all

    tools = galaxy_instance.tools.get_tools()

    if not all and not tool_ids:
        if not (name or display_name or owner):
            print('either name, display_name or owner must be specified')
            return
        if name and not fuzz:
            tools = [t for t in tools if t.get('tool_shed_repository') and t['tool_shed_repository']['name'] == name]
        if name and fuzz:
            tools = [t for t in tools if t.get('tool_shed_repository') and name in t['tool_shed_repository']['name']]
        if display_name:
            tools = [t for t in tools if display_name.lower() in t['name'].lower()]
        if version:
            tools = [t for t in tools if version in t['version']]
        if owner:
            tools = [t for t in tools if t.get('tool_shed_repository') and t['tool_shed_repository']['owner'] in owner]
    elif tool_ids:
        tools = [t for t in tools if t['id'] in tool_ids]
    if not tools:
        print('No tools found')
        return
    include_env = user_is_admin(galaxy_instance) and env

    def get_row(tool):
        row = [
            tool['name'],
            tool['tool_shed_repository']['name'] if tool.get('tool_shed_repository') else '-',
            tool['tool_shed_repository']['owner'] if tool.get('tool_shed_repository') else '-',
            tool['tool_shed_repository']['changeset_revision'] if tool.get('tool_shed_repository') else '-',
            tool['version'],
            tool['panel_section_name'],
            tool['id'],
        ]
        if include_env:
            row.append(get_env_from_requirements(galaxy_instance.tools.requirements(tool['id'])) or '-')
            if args.sleep:
                time.sleep(0.5)
        if biotools:
            xrefs = tool.get('xrefs')
            biotools_ids = [x['value'] for x in xrefs if x['reftype'] == 'bio.tools']
            row.append(' '.join(biotools_ids) if biotools_ids else '-')
        return row
    
    header = ['Display Name', 'Repo Name', 'Owner', 'Revision', 'Version', 'Section Label', 'Tool ID']
    if biotools:
        header.append('Biotools ID')
    if include_env:
        header.append('Environment')
    rows = [get_row(tool) for tool in tools]
 
    print('\t'.join(header))
    for row in rows:
        print('\t'.join([str(r) for r in row]))
