import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'gxtk-cat-bro',
    version = '0.0.1.dev0',
    author = 'Catherine B',
    author_email = 'cjbromheadATgmailDOTcom',
    description = 'Compact command line utility for galaxy API tool panel queries and more',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/cat-bro/gxtk',
    packages=setuptools.find_packages(),
    install_requires=[
        "galaxy-tool-util",
        "pysam",
        "bioblend>=0.17.0",  # TODO: parse requirements.txt file
    ],
    entry_points={
        'console_scripts': [
            'gxtk = src.gxtk:main'
        ]
    },
)