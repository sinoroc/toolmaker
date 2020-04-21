..


Introduction
============

Make single-file builds of Python tools using `zapp`_, `shiv`_, or `pex`_.


Repositories
------------

Binary distributions:

* https://pypi.org/project/toolmaker/

Source code:

* https://gitlab.com/sinoroc/toolmaker
* https://github.com/sinoroc/toolmaker


Usage
=====


.. code::

    $ toolmaker --help
    usage: toolmaker [-h] [--version] [--config CONFIG]
                     [--build | --rebuild | --delete] [--all]
                     [tool [tool ...]]

    Make single-file builds of Python tools using zapp, shiv, or pex

    positional arguments:
      tool                  apply action on this tool(s)

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --config CONFIG, -c CONFIG
                            configuration file (default:
                            /home/sinoroc/.config/toolmaker/toolmaker.cfg)
      --build, -b           build selected tool(s)
      --rebuild, -r         rebuild selected tool(s)
      --delete, -d          delete selected tool(s)
      --all, -a             apply action on all tools


Configuration
-------------

By default this tool looks for a configuration file at the following location:

* ``${HOME}/.config/toolmaker/toolmaker.cfg`` on *Linux*

* ``%USERPROFILE%\AppData\Roaming\toolmaker\toolmaker.cfg`` on *Windows*

.. code::

    [toolmaker.tool.defaults]
    tools_directory = ~/.local/bin/.toolmaker

    [toolmaker.tool.zapp:deptree]
    entry_point = deptree.cli:main
    requirements =
        deptree

    [toolmaker.tool.pex:http]
    entry_point = http.server

    [toolmaker.tool.shiv:shiv]
    entry_point = shiv.cli:main
    requirements =
        shiv

    [toolmaker.tool.zapp:something]
    entry_point = something.cli:main
    requirements =
        --no-index
        SomeRandomProject --find-links /path/to/location
    requirements_txts =
        requirements.txt
        more.txt


Action
------

The action can be specified on the command line. Either one of:

* ``--build``, ``-b`` to build (already existing tools are skipped);
* ``--rebuild``, ``-r`` to rebuild (already existing tools are rebuilt);
* ``--delete``, ``-d`` to delete (tool target file is deleted if it exists,
  then its parent directory is deleted if it is empty).

The default action when no flag is specified is to build the tools.


Configuration
=============

Place tools in current directory
--------------------------------

.. code::

    [toolmaker.tool.defaults]
    tools_directory =
    tool_directory =

    [toolmaker.tool.zapp:foo]
    # ./foo

    [toolmaker.tool.zapp:bar]
    # ./bar


Place tools in specific directory
---------------------------------

.. code::

    [toolmaker.tool.defaults]
    tools_directory = /somewhere
    tool_directory =

    [toolmaker.tool.zapp:foo]
    # /somewhere/foo

    [toolmaker.tool.zapp:bar]
    # /somewhere/bar


Place tools in subdirectories
-----------------------------

.. code::

    [toolmaker.tool.defaults]
    tools_directory = /somewhere

    [toolmaker.tool.zapp:foo0]
    # /somewhere/foo0/foo0

    [toolmaker.tool.zapp:foo1]
    tool_directory = foo0
    # /somewhere/foo0/foo1

    [toolmaker.tool.zapp:foo2]
    # /somewhere/foo2/foo2

    [toolmaker.tool.zapp:foo3]
    tool_file = foo0
    # /somewhere/foo3/foo0


Example to use with GNU stow
----------------------------

To use in combination with `GNU Stow`_:

.. code::

    [toolmaker.tool.defaults]
    tools_directory = ~/.local/bin/.toolmaker

    [toolmaker.tool.zapp:foo0]
    # ~/.local/bin/.toolmaker/foo0/foo0

    [toolmaker.tool.zapp:foo1]
    tool_directory = foo0
    # ~/.local/bin/.toolmaker/foo0/foo1

    [toolmaker.tool.zapp:foo2]
    # ~/.local/bin/.toolmaker/foo2/foo2

    [toolmaker.tool.zapp:foo3]
    tool_file = foo0
    # ~/.local/bin/.toolmaker/foo3/foo0



Details
=======

Similar projects
----------------

* `pickley`_
* `pipx`_
* `Zapper`_


.. Links

.. _`GNU Stow`: https://www.gnu.org/software/stow/
.. _`pex`: https://pypi.org/project/pex/
.. _`pickley`: https://pypi.org/project/pickley/
.. _`pipx`: https://pipxproject.github.io/pipx/
.. _`shiv`: https://pypi.org/project/shiv/
.. _`zapp`: https://pypi.org/project/zapp/
.. _`Zapper`: https://github.com/Valassis-Digital-Media/Zapper


.. EOF
