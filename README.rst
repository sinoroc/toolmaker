..


Introduction
============

This tool automates the build of Python tools according to a configuration
file. The tools can be built with `zapp`_, `shiv`_, or `pex`_.


Repositories
------------

Binary distributions:

* https://pypi.org/project/toolmaker/

Source code:

* https://gitlab.com/sinoroc/toolmaker
* https://github.com/sinoroc/toolmaker


Usage
=====

Configuration
-------------

By default this tool looks for a configuration file ``toolmaker.cfg`` in the
current working directory.

.. code::

    [toolmaker.tool.defaults]
    tools_directory = ~/.local/bin/.toolmaker

    [toolmaker.tool.zapp:deptree]
    entry_point = deptree.cli:main
    requirements =
        deptree

    [toolmaker.tool.pex:http]
    entry_point = http.server
    requirements =

    [toolmaker.tool.shiv:shiv]
    entry_point = shiv.cli:main
    requirements =
        shiv


Action
------

The action can be specified on the command line. Either one of:

* ``--build``, ``-b`` to build (already existing tools are skipped);
* ``--rebuild``, ``-r`` to rebuild (already existing tools are rebuilt);
* ``--delete``, ``-d`` to delete (tool target file is deleted if it exists, then
  its parent directory is deleted if it is empty).

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


Hacking
=======

This project makes extensive use of `tox`_, `pytest`_, and `GNU Make`_.


Development environment
-----------------------

Use following command to create a Python virtual environment with all
necessary dependencies::

    tox --recreate -e develop

This creates a Python virtual environment in the ``.tox/develop`` directory. It
can be activated with the following command::

    . .tox/develop/bin/activate


Run test suite
--------------

In a Python virtual environment run the following command::

    make review

Outside of a Python virtual environment run the following command::

    tox --recreate


Build and package
-----------------

In a Python virtual environment run the following command::

    make package

Outside of a Python virtual environment run the following command::

    tox --recreate -e package


.. Links

.. _`GNU Make`: https://www.gnu.org/software/make/
.. _`GNU Stow`: https://www.gnu.org/software/stow/
.. _`pex`: https://pypi.org/project/pex/
.. _`pickley`: https://pypi.org/project/pickley/
.. _`pipx`: https://pipxproject.github.io/pipx/
.. _`pytest`: https://pytest.org/
.. _`shiv`: https://pypi.org/project/shiv/
.. _`tox`: https://tox.readthedocs.io/
.. _`zapp`: https://pypi.org/project/zapp/
.. _`Zapper`: https://github.com/Valassis-Digital-Media/Zapper


.. EOF
