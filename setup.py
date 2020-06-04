#!/usr/bin/env python3

"""Setup script."""

import pathlib

import setuptools


def _get_version(file_name, line_number):
    here_path = pathlib.Path(__file__).resolve().parent
    with here_path.joinpath(file_name).open() as file_:
        changelog = file_.read()
    version = changelog.splitlines()[line_number]
    return version


def _main():
    setuptools.setup(
        # 'setup.cfg'
        version=_get_version('CHANGELOG.rst', 4),
    )


if __name__ == '__main__':
    _main()

# EOF
