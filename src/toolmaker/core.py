#


""" Core functionalities
"""


import logging
import os

import pex
import pex.bin.pex
import shiv
import shiv.cli
import zapp


LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _pex(requirements, entry_point, output_file_path):
    cmd = [
        '--entry-point={}'.format(entry_point),
        '--output-file={}'.format(str(output_file_path)),
    ] + requirements
    pex.bin.pex.main(cmd)


def _shiv(requirements, entry_point, output_file_path):
    # Since it is decorated by 'click', the 'main' function is not callable
    # with its original arguments. The original function is "hidden" under
    # 'callback'.
    shiv.cli.main.callback(
        str(output_file_path),  # output_file
        entry_point,  # entry_point
        None,  # console_script
        '/usr/bin/env python3',  # python
        None,  # site_packages
        True,  # compressed
        False,  # compile_pyc
        False,  # extend_pythonpath
        requirements,  # pip_args
    )


def _zapp(requirements, entry_point, output_file_path):
    zapp.core.build_zapp(requirements, entry_point, output_file_path)


def _get_requirements(config):
    requirements = [
        req.strip()
        for req in config['requirements'].splitlines()
        if req.strip()
    ]
    return requirements


def _get_output_file_path(work_dir_path, config):
    output_dir_path = work_dir_path.joinpath(config['name'])
    output_file_name = config['output_file']
    if os.name == 'nt' and 'output_file_win' in config:
        output_file_name = config['output_file_win']
    output_file_path = output_dir_path.joinpath(output_file_name)
    return output_file_path


def _build_pex(work_dir_path, config, force):
    """ Build pex
    """
    tool_name = config['name']
    output_file_path = _get_output_file_path(work_dir_path, config)
    if force or not output_file_path.exists():
        LOGGER.info("Building pex tool '%s'...", tool_name)
        requirements = _get_requirements(config)
        entry_point = config['entry_point']
        output_file_path.parent.mkdir(exist_ok=True)
        _pex(requirements, entry_point, output_file_path)
    else:
        LOGGER.info("Tool '%s' already exists, build skipped", tool_name)


def _build_shiv(work_dir_path, config, force):
    """ Build shiv
    """
    tool_name = config['name']
    output_file_path = _get_output_file_path(work_dir_path, config)
    if force or not output_file_path.exists():
        LOGGER.info("Building shiv tool '%s'...", tool_name)
        requirements = _get_requirements(config)
        entry_point = config['entry_point']
        output_file_path.parent.mkdir(exist_ok=True)
        _shiv(requirements, entry_point, output_file_path)
    else:
        LOGGER.info("Tool '%s' already exists, build skipped", tool_name)


def _build_zapp(work_dir_path, config, force):
    """ Build zapp
    """
    tool_name = config['name']
    output_file_path = _get_output_file_path(work_dir_path, config)
    if force or not output_file_path.exists():
        LOGGER.info("Building zapp tool '%s'...", tool_name)
        requirements = _get_requirements(config)
        entry_point = config['entry_point']
        output_file_path.parent.mkdir(exist_ok=True)
        _zapp(requirements, entry_point, output_file_path)
    else:
        LOGGER.info("Tool '%s' already exists, build skipped", tool_name)


TOOL_SECTION_NAMES = (
    'toolmaker.tool.pex',
    'toolmaker.tool.shiv',
    'toolmaker.tool.zapp',
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


def parse_config(raw_config):
    """ Parse the raw configration file to build a configuration dictionary.
    """
    config = {
        'tools': {},
    }
    for section_name in raw_config.sections():
        tool_config = _parse_tool_config(raw_config, section_name)
        if tool_config:
            config['tools'][tool_config['name']] = tool_config
    return config


def build(work_dir_path, config, tools_names, force=False):
    """ Build tools
    """
    LOGGER.info("Building tools %s...", tools_names)

    for tool_name in tools_names:
        if tool_name in config['tools']:
            tool_config = config['tools'][tool_name]
            if tool_config['type'] == 'pex':
                _build_pex(
                    work_dir_path,
                    tool_config,
                    force,
                )
            if tool_config['type'] == 'shiv':
                _build_shiv(
                    work_dir_path,
                    tool_config,
                    force,
                )
            if tool_config['type'] == 'zapp':
                _build_zapp(
                    work_dir_path,
                    tool_config,
                    force,
                )


def delete(work_dir_path, config, tools_names):
    """ Delete tools
    """
    LOGGER.info("Deleting tools %s...", tools_names)

    for tool_name in tools_names:
        if tool_name in config['tools']:
            tool_config = config['tools'][tool_name]
            output_file_path = _get_output_file_path(
                work_dir_path,
                tool_config,
            )
            if output_file_path.exists() and output_file_path.is_file():
                LOGGER.info("Deleting file '%s'", output_file_path)
                output_file_path.unlink()
            output_dir_path = output_file_path.parent
            if output_dir_path.exists() and output_dir_path.is_dir():
                LOGGER.info("Deleting directory '%s'", output_dir_path)
                try:
                    output_dir_path.rmdir()
                except OSError as ose:
                    import errno
                    if ose.errno == errno.ENOTEMPTY:
                        LOGGER.warning(
                            "Directory '%s' not empty",
                            output_dir_path,
                        )
                    else:
                        raise


# EOF
