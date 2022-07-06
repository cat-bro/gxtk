import setuptools

with open("README.md", "r") as handle:
    long_description = handle.read()

with open("requirements.txt") as handle:
    install_requires = handle.read().strip('\n').split('\n')
    print(install_requires)


setuptools.setup(
    name = 'gxtk-cat-bro',
    version = '0.0.1.dev0',
    author = 'Catherine B',
    author_email = 'cjbromheadATgmailDOTcom',
    description = 'Compact command line utility for galaxy API tool panel queries and miscellaneous helpers',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/cat-bro/gxtk',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'gxtk = gxtk.main:main',
        ]
    },
)