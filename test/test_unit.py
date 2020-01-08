""" Unit tests
"""


import tempfile
import unittest

import toolmaker


class TestProjectVersion(unittest.TestCase):
    """ Project version string
    """

    def test_project_has_version_string(self):
        """ Project should have a vesion string
        """
        try:
            toolmaker.__version__
        except AttributeError as version_exception:
            self.fail(version_exception)


def _make_config(str_config):
    config = None
    with tempfile.NamedTemporaryFile(mode='r+') as file_:
        file_.write(str_config)
        file_.seek(0)
        config = toolmaker.core.parse_config(file_)
    return config


def _get_path(config, tool_name):
    path = str(
        toolmaker.core._get_file_path(  # pylint: disable=protected-access
            config['tools'][tool_name],
        ),
    )
    return path


class TestGetFilePath(unittest.TestCase):
    """Test 'get_file_path'"""

    def test_get_file_path_one(self):
        """Install all in one specific directory"""
        str_config = """
        [toolmaker.tool.defaults]
        tools_directory = /somewhere
        tool_directory =

        [toolmaker.tool.zapp:foo]

        [toolmaker.tool.zapp:bar]
        """
        config = _make_config(str_config)
        self.assertEqual(
            _get_path(config, 'foo'),
            '/somewhere/foo',
        )
        self.assertEqual(
            _get_path(config, 'bar'),
            '/somewhere/bar',
        )

    def test_get_file_path_current(self):
        """Install all in current directory"""
        str_config = """
        [toolmaker.tool.defaults]
        tools_directory =
        tool_directory =

        [toolmaker.tool.zapp:foo]

        [toolmaker.tool.zapp:bar]
        """
        config = _make_config(str_config)
        self.assertEqual(
            _get_path(config, 'foo'),
            'foo',
        )
        self.assertEqual(
            _get_path(config, 'bar'),
            'bar',
        )

    def test_get_file_path_subfolder(self):
        """Install in subdirectories"""
        str_config = """
        [toolmaker.tool.defaults]
        tools_directory = /somewhere

        [toolmaker.tool.zapp:foo0]

        [toolmaker.tool.zapp:foo1]
        tool_directory = foo0

        [toolmaker.tool.zapp:foo2]

        [toolmaker.tool.zapp:foo3]
        tool_file = foo0
        """
        config = _make_config(str_config)
        self.assertEqual(
            _get_path(config, 'foo0'),
            '/somewhere/foo0/foo0',
        )
        self.assertEqual(
            _get_path(config, 'foo1'),
            '/somewhere/foo0/foo1',
        )
        self.assertEqual(
            _get_path(config, 'foo2'),
            '/somewhere/foo2/foo2',
        )
        self.assertEqual(
            _get_path(config, 'foo3'),
            '/somewhere/foo3/foo0',
        )


# EOF
