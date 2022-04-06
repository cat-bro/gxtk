# tool-panel-scripts
Scripts for querying the galaxy tool panel

**get_tool_details.py**

Filter a list of all installed tools on Galaxy based on repository name or tool display name.  Results are returned as
tab separated values.  If an admin API key is supplied, the result includes the name of the tool's conda environment if
there is one.

```
usage: get_tool_details.py [-h] [-n NAME] [-N DISPLAY_NAME] [-v VERSION] [-o OWNER] [-z] [--all] [-e] [-g GALAXY_URL] [-a API_KEY] [-p PROFILE] [-t TOOL_IDS [TOOL_IDS ...]] [-s]

Search for tools on Galaxy using repository name or tool display name

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Tool repository name
  -N DISPLAY_NAME, --display_name DISPLAY_NAME
                        User facing tool name
  -v VERSION, --version VERSION
                        Version
  -o OWNER, --owner OWNER
                        Owner
  -z, --fuzz            Match substring of repository name from search term
  --all                 Show all installed tools
  -e, --env             Show virtual environment name (admin API key required)
  -g GALAXY_URL, --galaxy_url GALAXY_URL
                        URL of Galaxy instance
  -a API_KEY, --api_key API_KEY
                        Galaxy api key
  -p PROFILE, --profile PROFILE
                        Key for profile set in profiles.yml
  -t TOOL_IDS [TOOL_IDS ...], --tool_ids TOOL_IDS [TOOL_IDS ...]
                        One or more tool ids to match exactly
  -s, --sleep           Sleep for 0.5s after fetching requirements
```