## gxtk
Command line program querying the galaxy tool panel and performing miscellaneous tasks on galaxy instances.
[gxtk docs](https://gxtk.readthedocs.io/en/latest/gxtk.html#)

### Installation:

Installation within a virtual environment is recommended.

##### Install with pip

`pip install git+https://github.com/cat-bro/gxtk.git`

##### Alternative to installing with pip

Clone this repository.  `python gxtk.py` in the root directory can be run in place of `gxtk` provided that the requirements are installed.

### Galaxy authentication and configuration file

`gxtk` has command line options --galaxy_url (-g) and --api_key (-a) for logging into galaxy. 
Alternatively the command line option --profile (-p) can be used to select a profile from 
a configuration file with the path ~/.gxtk.yml. The location of the file can be overriden
by setting the `GXTK_PROFILES_PATH` environment variable or using the --profiles_path
command line option.  gxtk uses the `parsec` style of configuration, with a yaml key
for each profile and either `url` or `url` and `key` set for profile.  The default profile
key is set with the key `__default`.
See [example profiles file](.gxtk.yml.sample)

To download the sample file
```
wget https://raw.githubusercontent.com/cat-bro/gxtk/main/.gxtk.yml.sample
mv .gxtk.yml.sample .gxtk.yml
```

**[gxtk find](https://gxtk.readthedocs.io/en/latest/gxtk.html#find)**

Filter a list of installed tools on Galaxy based on repository name or tool display name.  Results are returned as
tab separated values.  If an admin API key is supplied and the -e flag included, the result includes the name of the
tool's conda environment.
