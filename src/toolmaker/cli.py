#


""" Command line interface """


import argparse
import configparser
import logging
import pathlib

from . import core
from . import meta


def _create_args_parser(default_config_path, tools_names=None):
    args_parser = argparse.ArgumentParser(
        allow_abbrev=False,
    )
    args_parser.add_argument(
        '--version',
        action='version',
        version=meta.VERSION,
    )
    args_parser.add_argument(
        '--config', '-c',
        default=str(default_config_path),
        type=argparse.FileType('r'),
    )
    group = args_parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--all', '-a',
        action='store_true',
    )
    group.add_argument(
        '--tools', '-t',
        choices=tools_names,
        metavar='tool',
        nargs='+',
    )
    return args_parser


def main():
    """ CLI main function
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    cwd_path = pathlib.Path.cwd()
    default_config_path = cwd_path.joinpath('toolmaker.cfg')

    args_parser = _create_args_parser(default_config_path)
    args = args_parser.parse_args()

    config = None
    if args.config:
        config = configparser.ConfigParser()
        try:
            config.read_file(args.config)
        except configparser.Error as config_error:
            args_parser.error(config_error)
    tools_names = config.sections()

    if not args.all:
        args_parser = _create_args_parser(default_config_path, tools_names)
        args = args_parser.parse_args()

    if args.tools:
        tools_names = args.tools

    logger.info("Preparing to build tools %s", tools_names)

    venv_path = cwd_path.joinpath('venv')

    logger.info("Creating virtual environment '%s'...", venv_path)
    venv_context = core.venv_create(venv_path)

    logger.info("Updating virtual environment")
    core.venv_update(venv_context)

    for tool_name in tools_names:
        if tool_name.endswith('.pex'):
            logger.info("Building pex tool '%s'", tool_name)
            core.build_pex(cwd_path, venv_context, config, tool_name)
        if tool_name.endswith('.shiv'):
            logger.info("Building shiv tool '%s'", tool_name)
            core.build_shiv(cwd_path, venv_context, config, tool_name)
        if tool_name.endswith('.zapp'):
            logger.info("Building zapp tool '%s'", tool_name)
            core.build_zapp(cwd_path, venv_context, config, tool_name)


# EOF
