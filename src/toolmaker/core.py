#


""" Core functionalities
"""


import pathlib
import subprocess
import venv


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


def build_pex(cwd_path, venv_context, config, section_name):
    """ Build pex
    """
    section = config[section_name]
    output_dir_path = cwd_path.joinpath(section_name)
    output_dir_path.mkdir(exist_ok=True)
    output_file_name = section['output_file']
    output_file_path = output_dir_path.joinpath(output_file_name)
    requirements = [
        req for req in section['requirements'].splitlines() if req
    ]
    entry_point = section['entry_point']
    _pex(venv_context, entry_point, output_file_path, requirements)


def build_shiv(cwd_path, venv_context, config, section_name):
    """ Build shiv
    """
    section = config[section_name]
    output_dir_path = cwd_path.joinpath(section_name)
    output_dir_path.mkdir(exist_ok=True)
    output_file_name = section['output_file']
    output_file_path = output_dir_path.joinpath(output_file_name)
    requirements = [
        req for req in section['requirements'].splitlines() if req
    ]
    console_script = section['console_script']
    _shiv(venv_context, console_script, output_file_path, requirements)


def build_zapp(cwd_path, venv_context, config, section_name):
    """ Build zapp
    """
    section = config[section_name]
    output_dir_path = cwd_path.joinpath(section_name)
    output_dir_path.mkdir(exist_ok=True)
    output_file_name = section['output_file']
    output_file_path = output_dir_path.joinpath(output_file_name)
    requirements = [
        req for req in section['requirements'].splitlines() if req
    ]
    entry_point = section['entry_point']
    _zapp(venv_context, output_file_path, entry_point, requirements)


class _EnvBuilder(venv.EnvBuilder):

    def __init__(self, *args, **kwargs):
        self.context = None
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """ Override """
        self.context = context


def venv_create(venv_path):
    """ Create virtual environment
    """
    venv_builder = _EnvBuilder(with_pip=True)
    venv_builder.create(venv_path)
    return venv_builder.context


def venv_update(venv_context):
    """ Update virtual environment
    """
    _pip_install(venv_context, ['pip'])
    _pip_install(venv_context, ['setuptools'])
    _pip_install(venv_context, ['pex[cachecontrol,requests]', 'shiv', 'zapp'])


# EOF
