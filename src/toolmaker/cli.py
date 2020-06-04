#

"""Command line interface."""

import argparse

from . import _i18n
from . import _meta
from . import core

_ = _i18n._


def _create_args_parser(default_config_path, tools_names=None):
    args_parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description=_meta.SUMMARY,
    )
    args_parser.add_argument(
        '--version',
        action='version',
        version=_meta.VERSION,
    )
    args_parser.add_argument(
        '--config',
        '-c',
        default=str(default_config_path),
        help=_("configuration file (default: {})").format(default_config_path),
        type=argparse.FileType('r'),
    )
    action_group = args_parser.add_mutually_exclusive_group()
    action_group.add_argument(
        '--build',
        '-b',
        action='store_true',
        help=_("build selected tool(s)"),
    )
    action_group.add_argument(
        '--rebuild',
        '-r',
        action='store_true',
        help=_("rebuild selected tool(s)"),
    )
    action_group.add_argument(
        '--delete',
        '-d',
        action='store_true',
        help=_("delete selected tool(s)"),
    )
    args_parser.add_argument(
        '--all',
        '-a',
        action='store_true',
        help=_("apply action on all tools"),
    )
    args_parser.add_argument(
        'tools',
        choices=tools_names,
        help=_("apply action on this tool(s)"),
        metavar='tool',
        nargs='*',
    )
    return args_parser


def main():
    """Create and run CLI application."""
    default_config_path = core.get_default_config_file_path()

    args_parser = _create_args_parser(default_config_path)
    args = args_parser.parse_args()

    config = None
    if args.config:
        try:
            config = core.parse_config(args.config)
        except core.CanNotParseConfigurationFile as config_error:
            args_parser.error(config_error)
        else:
            tools_names = list(config['tools'].keys())
            if not args.all:
                args_parser = _create_args_parser(
                    default_config_path,
                    tools_names,
                )
                args = args_parser.parse_args()

            if args.tools:
                tools_names = args.tools

            if args.delete:
                core.delete(config, tools_names)
            elif args.rebuild:
                core.build(config, tools_names, force=True)
            else:
                core.build(config, tools_names)


# EOF
