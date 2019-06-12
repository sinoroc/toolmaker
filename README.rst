..


Introduction
============

This tool automates the build of Python tools according to a configuration
file. The tools can be built with `zapp`_, `shiv`_, or `pex`_.


Repositories
------------

Binary distributions:

* http://pypi.org/project/toolmaker/

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

    [http.pex]
    entry_point = http.server
    output_file = http
    requirements =

    [pipdeptree.zapp]
    entry_point = pipdeptree:main
    output_file = pipdeptree
    requirements =
        pipdeptree
        setuptools

    [shiv.shiv]
    console_script = shiv
    output_file = shiv
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


Tips
----

Place in a subdirectory of a directory that is available on your ``PATH``
(typically your ``~/bin`` directory) and use in combination with `GNU Stow`_.


Details
=======

Similar projects
----------------

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
.. _`pytest`: https://pytest.org/
.. _`shiv`: https://pypi.org/project/shiv/
.. _`tox`: https://tox.readthedocs.io/
.. _`zapp`: https://pypi.org/project/zapp/
.. _`Zapper`: https://github.com/Valassis-Digital-Media/Zapper


.. EOF
