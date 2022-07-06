"""
Reload a tool without having to restart Galaxy.  This requires an admin API key.
"""

def reload_tool(galaxy_instance, args):
    galaxy_instance.tools.reload(args.tool_id)
