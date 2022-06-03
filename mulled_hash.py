import hashlib
import argparse

# Adapted from this gist by natefoo: https://gist.github.com/natefoo/7a13e5bf6f4bbf961db73a3d6e9f9e1c
# and https://github.com/galaxyproject/galaxy/blob/release_21.01/lib/galaxy/tool_util/deps/conda_util.py

# Generate Galaxy Conda mulled hashes from a list of requirements


def main():
    parser = argparse.ArgumentParser(description='Get a Galaxy style virtual environment name from a list of conda requirements')
    parser.add_argument('requirements', help='One or more conda requirements e.g. balloon=1.1 or fish=3.2b', nargs='+')
    args = parser.parse_args()
    targets = []
    for req in args.requirements:
        if '=' in req:
            name, version = req.split('=')
        else:
            name, version = [req, None]
        targets.append((name, version))
    print(get_env_name(targets))


def install_environment(target):
    package, version = target
    if version:
        return "__%s@%s" % (package, version)
    else:
        return "__%s@_uv_" % (package)


def hash_conda_packages(targets):
    h = hashlib.new('sha256')
    for target in targets:
        h.update(install_environment(target).encode('utf-8'))
    return h.hexdigest()


def get_env_name(targets):
    if len(targets) == 1:
        return install_environment(targets[0])
    else:
        return 'mulled-v1-' + hash_conda_packages(targets)


if __name__ == '__main__':
    main()
