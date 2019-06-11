#


""" Core functionalities
"""


import logging
import pathlib
import subprocess
import venv


LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _run_in_venv(venv_context, command):
    venv_bin_path = pathlib.Path(venv_context.bin_path)
    command_in_venv = [
        str(venv_bin_path.joinpath(command[0])),
    ] + command[1:]
    subprocess.run(command_in_venv)


def _pip_install(venv_context, packages):
    command = [
        'pip',
        'install',
        '--upgrade',
    ] + packages
    _run_in_venv(venv_context, command)


def _pex(venv_context, entry_point, output_file_path, requirements):
    _run_in_venv(
        venv_context,
        [
            'pex',
            '--entry-point={}'.format(entry_point),
            '--output-file={}'.format(str(output_file_path)),
        ] + requirements,
    )


def _shiv(venv_context, console_script, output_file_path, requirements):
    _run_in_venv(
        venv_context,
        [
            'shiv',
            '--console-script',
            console_script,
            '--output-file',
            str(output_file_path),
        ] + requirements,
    )


def _zapp(venv_context, output_file_path, entry_point, requirements):
    _run_in_venv(
        venv_context,
        [
            'zapp',
            output_file_path,
            entry_point,
        ] + requirements,
    )


def _get_requirements(config):
    requirements = [
        req.strip()
        for req in config['requirements'].splitlines()
        if req.strip()
    ]
    return requirements


def _get_output_file_path(work_dir_path, tool_name, config):
    output_dir_path = work_dir_path.joinpath(tool_name)
    output_file_name = config['output_file']
    output_file_path = output_dir_path.joinpath(output_file_name)
    return output_file_path


def build_pex(work_dir_path, venv_context, tool_name, config, force):
    """ Build pex
    """
    output_file_path = _get_output_file_path(work_dir_path, tool_name, config)
    if force or not output_file_path.exists():
        requirements = _get_requirements(config)
        entry_point = config['entry_point']
        output_file_path.parent.mkdir(exist_ok=True)
        _pex(venv_context, entry_point, output_file_path, requirements)
    else:
        LOGGER.info("Tool '%s' already exists, build skipped", tool_name)


def build_shiv(work_dir_path, venv_context, tool_name, config, force):
    """ Build shiv
    """
    output_file_path = _get_output_file_path(work_dir_path, tool_name, config)
    if force or not output_file_path.exists():
        requirements = _get_requirements(config)
        console_script = config['console_script']
        output_file_path.parent.mkdir(exist_ok=True)
        _shiv(venv_context, console_script, output_file_path, requirements)
    else:
        LOGGER.info("Tool '%s' already exists, build skipped", tool_name)


def build_zapp(work_dir_path, venv_context, tool_name, config, force):
    """ Build zapp
    """
    output_file_path = _get_output_file_path(work_dir_path, tool_name, config)
    if force or not output_file_path.exists():
        requirements = _get_requirements(config)
        entry_point = config['entry_point']
        output_file_path.parent.mkdir(exist_ok=True)
        _zapp(venv_context, output_file_path, entry_point, requirements)
    else:
        LOGGER.info("Tool '%s' already exists, build skipped", tool_name)


def build(work_dir_path, config, tools_names, force=False):
    """ Build tools
    """
    LOGGER.info("Preparing to build tools %s", tools_names)
    venv_path = work_dir_path.joinpath('venv')

    LOGGER.info("Creating virtual environment '%s'...", venv_path)
    venv_context = _venv_create(venv_path)

    LOGGER.info("Updating virtual environment")
    _venv_update(venv_context)

    for tool_name in tools_names:
        tool_config = config[tool_name]
        if tool_name.endswith('.pex'):
            LOGGER.info("Building pex tool '%s'", tool_name)
            build_pex(
                work_dir_path,
                venv_context,
                tool_name,
                tool_config,
                force,
            )
        if tool_name.endswith('.shiv'):
            LOGGER.info("Building shiv tool '%s'", tool_name)
            build_shiv(
                work_dir_path,
                venv_context,
                tool_name,
                tool_config,
                force,
            )
        if tool_name.endswith('.zapp'):
            LOGGER.info("Building zapp tool '%s'", tool_name)
            build_zapp(
                work_dir_path,
                venv_context,
                tool_name,
                tool_config,
                force,
            )


def delete(work_dir_path, config, tools_names):
    """ Delete tools
    """
    LOGGER.info("Deleting tools %s", tools_names)

    for tool_name in tools_names:
        output_file_path = _get_output_file_path(
            work_dir_path,
            tool_name,
            config[tool_name],
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
                    LOGGER.warning("Directory '%s' not empty", output_dir_path)
                else:
                    raise


class _EnvBuilder(venv.EnvBuilder):

    def __init__(self, *args, **kwargs):
        self.context = None
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """ Override """
        self.context = context


def _venv_create(venv_path):
    """ Create virtual environment
    """
    venv_builder = _EnvBuilder(with_pip=True)
    venv_builder.create(venv_path)
    return venv_builder.context


def _venv_update(venv_context):
    """ Update virtual environment
    """
    _pip_install(venv_context, ['pip'])
    _pip_install(venv_context, ['setuptools'])
    _pip_install(venv_context, ['pex[cachecontrol,requests]', 'shiv', 'zapp'])


# EOF
