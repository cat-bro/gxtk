## gxtk
Scripts for querying the galaxy tool panel

### Installation:

Clone this repository.  Optionally add the line `source <path to .bashrc_helper>` to .bashrc/.zshrc to be able to use the alias `gxtk` in place of get_tool_details.py.

#### profiles.yml

Copy profiles.yml.sample to profiles.yml to use `-p <profile>` in command line in place of `-g <galaxy_url> -a <api_key>`.  The default profile will be used when none of `--galaxy_url (-g)`, `--api_key (-a)` or `--profile (p)` are provided. 

**get_tool_details.py**

Filter a list of all installed tools on Galaxy based on repository name or tool display name.  Results are returned as
tab separated values.  If an admin API key is supplied and the -e flag included, the result includes the name of the
tool's conda environment.

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
  -b, --biotools        Show bio.tools IDs in output
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

##### Example: find all versions of bwameth on Galaxy Australia Dev:
```
$ gxtk -g https://dev.usegalaxy.org.au -n bwameth
Display Name	Repo name	Owner	Revision	Version	Section Label	Tool ID
bwameth	bwameth	iuc	b4e6819b25ef	0.2.2+galaxy1	Epigenetics	toolshed.g2.bx.psu.edu/repos/iuc/bwameth/bwameth/0.2.2+galaxy1
bwameth	bwameth	iuc	62f5fab76dfb	0.2.3+galaxy0	Epigenetics	toolshed.g2.bx.psu.edu/repos/iuc/bwameth/bwameth/0.2.3+galaxy0
```

##### Example: find all versions of bwameth on Galaxy Australia Dev with name of conda virtual environment (requires admin api key):
```
$ gxtk -g https://dev.usegalaxy.org.au -a <admin api key> -n bwameth -e
Display Name	Repo name	Owner	Revision	Version	Section Label	Tool ID	Environment
bwameth	bwameth	iuc	b4e6819b25ef	0.2.2+galaxy1	Epigenetics	toolshed.g2.bx.psu.edu/repos/iuc/bwameth/bwameth/0.2.2+galaxy1	__bwameth@0.2.2
bwameth	bwameth	iuc	62f5fab76dfb	0.2.3+galaxy0	Epigenetics	toolshed.g2.bx.psu.edu/repos/iuc/bwameth/bwameth/0.2.3+galaxy0	__bwameth@0.2.3
```

##### Find tools owned by qfabrepo or galaxy-australia on Galaxy Australia using --profile (-p) argument:
```
$ gxtk -p au -o galaxy-australia qfabrepo
Display Name	Repo name	Owner	Revision	Version	Section Label	Tool ID
Hapcut2	hapcut2	galaxy-australia	271eb7f4b8bc	1.3.3+galaxy0+ga1	Assembly	toolshed.g2.bx.psu.edu/repos/galaxy-australia/hapcut2/hapcut2/1.3.3+galaxy0+ga1
Smudgeplot	smudgeplot	galaxy-australia	e53b0473d575	0.2.5+galaxy+1	Assembly	toolshed.g2.bx.psu.edu/repos/galaxy-australia/smudgeplot/smudgeplot/0.2.5+galaxy+1
PEAR Statistics	metadegalaxy_pear_stats	qfabrepo	ec62f17fcfe6	1.0.0	Metagenomic Analysis	toolshed.g2.bx.psu.edu/repos/qfabrepo/metadegalaxy_pear_stats/pearStat/1.0.0
Phyloseq Abundance plot	metadegalaxy_phyloseq_abundance_factor	qfabrepo	3856a1590a11	1.22.3.3	Metagenomic Analysis	toolshed.g2.bx.psu.edu/repos/qfabrepo/metadegalaxy_phyloseq_abundance_factor/phyloseq_abundance/1.22.3.3
Phyloseq Abundance Taxonomy	metadegalaxy_phyloseq_abundance_taxonomy	qfabrepo	b2fafdd3533d	1.22.3.3	Metagenomic Analysis	toolshed.g2.bx.psu.edu/repos/qfabrepo/metadegalaxy_phyloseq_abundance_taxonomy/phyloseq_taxonomy/1.22.3.3
Phyloseq DESeq2	metadegalaxy_phyloseq_deseq2	qfabrepo	7e24242ffa65	1.22.3	Metagenomic Analysis	toolshed.g2.bx.psu.edu/repos/qfabrepo/metadegalaxy_phyloseq_deseq2/phyloseq_DESeq2/1.22.3
Phyloseq Network Plot	metadegalaxy_phyloseq_net	qfabrepo	22abc415e142	1.24.2	Metagenomic Analysis	toolshed.g2.bx.psu.edu/repos/qfabrepo/metadegalaxy_phyloseq_net/phyloseq_net/1.24.2
Phyloseq Richness	metadegalaxy_phyloseq_richness	qfabrepo	e0225f3e8ef6	1.22.3.2	Metagenomic Analysis	toolshed.g2.bx.psu.edu/repos/qfabrepo/metadegalaxy_phyloseq_richness/phyloseq_richness/1.22.3.2
reheader	metadegalaxy_reheader	qfabrepo	dce768959840	1.0.0	Metagenomic Analysis	toolshed.g2.bx.psu.edu/repos/qfabrepo/metadegalaxy_reheader/rename/1.0.0
Symmetric Plot	metadegalaxy_symmetric_plot	qfabrepo	91fb94d203df	1.0.1	Metagenomic Analysis	toolshed.g2.bx.psu.edu/repos/qfabrepo/metadegalaxy_symmetric_plot/symmetricPlot/1.0.1
OTUTable	metadegalaxy_uc2otutable	qfabrepo	08ca35e99b74	1.0.0	Metagenomic Analysis	toolshed.g2.bx.psu.edu/repos/qfabrepo/metadegalaxy_uc2otutable/uclust2otutable/1.0.0
Alphafold 2	alphafold2	galaxy-australia	eb085b3dbaf8	2.1.2+galaxy0	Proteomic AI	toolshed.g2.bx.psu.edu/repos/galaxy-australia/alphafold2/alphafold/2.1.2+galaxy0
```