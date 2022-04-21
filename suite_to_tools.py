import argparse
import yaml
from pprint import pprint

from bioblend.toolshed import ToolShedInstance

def main():
    parser = argparse.ArgumentParser(description='Get list of tools from suite url or name/owner/revision/tool_shed_url of tool suite')
    parser.add_argument('-n', '--name', help='Suite name')
    parser.add_argument('-o', '--owner', help='Suite owner')
    parser.add_argument('-r', '--revision', help='Suite revision')
    parser.add_argument('-t', '--tool_shed_url', help='Suite tool shed url', default='toolshed.g2.bx.psu.edu')
    parser.add_argument('-s', '--section_label', help='Section label')
    parser.add_argument('-u', '--url', help='Link to tool shed repository')
    args = parser.parse_args()

    if args.name and args.revision and args.owner:
        name = args.name
        owner = args.owner
        revision = args.revision
        tool_shed_url = args.tool_shed_url
    elif args.url:
        url = args.url
        if url.startswith('https://'):
            url = url.split('//')[1]
        tool_shed_url, _, owner, name, revision = url.strip('/').split('/')
    else:
        raise Exception('--url argument or all of --name, --owner and --revision must be provided')

    shed = ToolShedInstance('https://'+tool_shed_url)

    aa, metadata, install_info = shed.repositories.get_repository_revision_install_info(name, owner, revision)
    _1, _2, _3, _4, _5, rev_info_1, rev_info_2 = install_info[name]

    tools = []

    for key in rev_info_1:
        if key.startswith(tool_shed_url):
            list_of_lists = rev_info_1[key]
            for el in list_of_lists:
                    tools.append({
                        'name': el[1],
                        'owner': el[2],
                        'revisions': [el[3]],
                        'tool_panel_section_label': args.section_label or '??',
                        'tool_shed_url': tool_shed_url,
                    })

    with open(name + '_list.yml', 'w') as handle:
        yaml.dump({'tools': tools}, handle)


if __name__ == '__main__':
    main()