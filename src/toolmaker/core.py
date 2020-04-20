#


""" Core functionalities
"""


import configparser
import errno
import logging
import os
import pathlib
import platform
import tempfile

import pex.bin.pex
import shiv
import shiv.cli
import zapp

from . import _meta


LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ConfigurationFileError(configparser.Error):
    """Configuration file error"""


def _pex(requirements_txts, entry_point, output_file_path):
    command = [
        '--entry-point={}'.format(entry_point),
        '--output-file={}'.format(str(output_file_path)),
    ] + [
        '--requirement={}'.format(requirements_txt)
        for requirements_txt
        in requirements_txts
    ]
    pex.bin.pex.main(command)


def _shiv(requirements_txts, entry_point, output_file_path):
    pip_args = []
    for requirements_txt in requirements_txts:
        pip_args.extend(
            [
                '--requirement',
                requirements_txt,
            ],
        )
    # Since it is decorated by 'click', the 'main' function is not callable
    # with its original arguments. The original function is "hidden" under
    # 'shiv.cli.main.callback'. And 'shiv.cli.main' takes the equivalent of
    # 'sys.argv' instead, but running it causes the whole application to exit
    # at the end of the 'shiv.cli.main' function call.
    shiv.cli.main.callback(
        output_file=str(output_file_path),
        entry_point=entry_point,
        console_script=None,
        python='/usr/bin/env python3',
        site_packages=None,
        compressed=False,
        compile_pyc=False,
        extend_pythonpath=False,
        reproducible=False,
        pip_args=pip_args,
    )


def _zapp(requirements_txts, entry_point, output_file_path):
    zapp.core.build_zapp(
        output_file_path,
        entry_point,
        requirements_txts=requirements_txts,
    )


def _get_requirements_txts(tool_config, temp_requirements_txt):
    requirements_txts = []
    #
    requirements = tool_config.get('requirements', None)
    if requirements:
        temp_requirements_txt.write(requirements)
        temp_requirements_txt.flush()
        requirements_txts.append(temp_requirements_txt.name)
    #
    for line in tool_config.get('requirements_txts', '').splitlines():
        stripped_line = line.strip()
        if stripped_line:
            requirements_txt_path = pathlib.Path(stripped_line)
            requirements_txts.append(
                str(requirements_txt_path)
                if requirements_txt_path.is_absolute()
                else str(
                    tool_config['configuration_directory'].joinpath(
                        requirements_txt_path,
                    )
                )
            )
    #
    return requirements_txts


def _get_file_path(tool_config):
    path = (
        pathlib.Path(
            os.path.expandvars(tool_config['tools_directory']),
        ).expanduser()
        if 'tools_directory' in tool_config
        else pathlib.Path.cwd()
    )

    if 'tool_directory' in tool_config:
        tool_directory_name = tool_config['tool_directory']
        if tool_directory_name:
            path = path.joinpath(tool_directory_name)
    else:
        path = path.joinpath(tool_config['name'])

    if 'tool_file' in tool_config:
        path = path.joinpath(tool_config['tool_file'])
    else:
        path = path.joinpath(tool_config['name'])

    if platform.system() == 'Windows':
        path = path.with_suffix('.pyz')

    return path


def _build_pex(tool_config, force):
    """ Build pex
    """
    tool_name = tool_config['name']
    output_file_path = _get_file_path(tool_config)
    if force or not output_file_path.exists():
        LOGGER.info("Building pex tool '%s'...", tool_name)
        entry_point = tool_config['entry_point']
        output_file_path.parent.mkdir(exist_ok=True)
        with tempfile.NamedTemporaryFile('w') as temp_requirements_txt:
            requirements_txts = _get_requirements_txts(
                tool_config,
                temp_requirements_txt,
            )
            _pex(requirements_txts, entry_point, output_file_path)
    else:
        LOGGER.info("Tool '%s' already exists, build skipped", tool_name)


def _build_shiv(tool_config, force):
    """ Build shiv
    """
    tool_name = tool_config['name']
    output_file_path = _get_file_path(tool_config)
    if force or not output_file_path.exists():
        LOGGER.info("Building shiv tool '%s'...", tool_name)
        entry_point = tool_config['entry_point']
        output_file_path.parent.mkdir(exist_ok=True)
        with tempfile.NamedTemporaryFile('w') as temp_requirements_txt:
            requirements_txts = _get_requirements_txts(
                tool_config,
                temp_requirements_txt,
            )
            _shiv(requirements_txts, entry_point, output_file_path)
    else:
        LOGGER.info("Tool '%s' already exists, build skipped", tool_name)


def _build_zapp(tool_config, force):
    """ Build zapp
    """
    tool_name = tool_config['name']
    output_file_path = _get_file_path(tool_config)
    if force or not output_file_path.exists():
        LOGGER.info("Building zapp tool '%s'...", tool_name)
        entry_point = tool_config['entry_point']
        output_file_path.parent.mkdir(exist_ok=True)
        with tempfile.NamedTemporaryFile('w') as temp_requirements_txt:
            requirements_txts = _get_requirements_txts(
                tool_config,
                temp_requirements_txt,
            )
            _zapp(requirements_txts, entry_point, output_file_path)
    else:
        LOGGER.info("Tool '%s' already exists, build skipped", tool_name)


TOOL_SECTION_NAMES = (
    '{}.tool.pex'.format(_meta.PROJECT_NAME),
    '{}.tool.shiv'.format(_meta.PROJECT_NAME),
    '{}.tool.zapp'.format(_meta.PROJECT_NAME),
)


def _parse_tool_config(raw_config, section_name):
    tool_config = None
    tokens = section_name.split(':', maxsplit=1)
    if len(tokens) == 2 and tokens[0] in TOOL_SECTION_NAMES:
        tool_config = {
            'name': tokens[1],
            'type': tokens[0].split('.')[2],
        }
        tool_config.update(raw_config[section_name])
    return tool_config


def parse_config(config_file):
    """ Parse the configuration file to build a configuration dictionary
    """
    config = None
    raw_config = configparser.ConfigParser(
        default_section='{}.tool.defaults'.format(_meta.PROJECT_NAME),
        interpolation=configparser.ExtendedInterpolation(),
    )
    try:
        LOGGER.info("Read configuration from '%s'", config_file.name)
        raw_config.read_file(config_file)
    except configparser.Error as config_error:
        LOGGER.error(
            "Can not read configuration from file '%s'",
            config_file.name,
        )
        raise ConfigurationFileError(str(config_error))
    else:
        config_directory_path = pathlib.Path(config_file.name).resolve().parent
        config = {
            'tools': {},
        }
        for section_name in raw_config.sections():
            tool_config = _parse_tool_config(
                raw_config,
                section_name,
            )
            if tool_config:
                tool_config['configuration_directory'] = config_directory_path
                config['tools'][tool_config['name']] = tool_config
    return config


def build(config, tools_names, force=False):
    """ Build tools
    """
    LOGGER.info("Building tools %s...", tools_names)

    for tool_name in tools_names:
        if tool_name in config['tools']:
            tool_config = config['tools'][tool_name]
            if tool_config['type'] == 'pex':
                _build_pex(
                    tool_config,
                    force,
                )
            if tool_config['type'] == 'shiv':
                _build_shiv(
                    tool_config,
                    force,
                )
            if tool_config['type'] == 'zapp':
                _build_zapp(
                    tool_config,
                    force,
                )


def delete(config, tools_names):
    """ Delete tools
    """
    LOGGER.info("Deleting tools %s...", tools_names)

    for tool_name in tools_names:
        if tool_name in config['tools']:
            tool_config = config['tools'][tool_name]
            output_file_path = _get_file_path(tool_config)
            if output_file_path.exists() and output_file_path.is_file():
                LOGGER.info("Deleting file '%s'", output_file_path)
                output_file_path.unlink()
            output_dir_path = output_file_path.parent
            if output_dir_path.exists() and output_dir_path.is_dir():
                LOGGER.info("Deleting directory '%s'", output_dir_path)
                try:
                    output_dir_path.rmdir()
                except OSError as ose:
                    if ose.errno == errno.ENOTEMPTY:
                        LOGGER.warning(
                            "Directory '%s' not empty",
                            output_dir_path,
                        )
                    else:
                        raise


def get_default_config_file_path():
    """ Get default path for configuration file
        Depends on the operating system.
    """
    file_name = 'toolmaker.cfg'
    dir_name = _meta.PROJECT_NAME
    path = None
    config_path = None
    system = platform.system()
    if system == 'Windows':
        if 'APPDATA' in os.environ:
            config_path = pathlib.Path(os.environ['APPDATA'])
        else:
            config_path = pathlib.Path.home().joinpath('AppData', 'Roaming')
    elif system == 'Linux':
        if 'XDG_CONFIG_HOME' in os.environ:
            config_path = pathlib.Path(os.environ['XDG_CONFIG_HOME'])
        else:
            config_path = pathlib.Path.home().joinpath('.config')
    if config_path:
        path = config_path.joinpath(dir_name, file_name)
    return path


# EOF
