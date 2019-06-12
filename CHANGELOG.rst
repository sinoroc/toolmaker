..


.. Keep the current version number on line number 5
0.0.1
=====

2019-06-12

* Add action as CLI optional argument. The action has to be specified on the
  command line. Either one of:

  * ``--build``, ``-b`` to build (existing tools are skipped);
  * ``--rebuild``, ``-r`` to rebuild (existing tools are rebuilt);
  * ``--delete``, ``-d`` to delete (tool target file is deleted if it exists,
    its parent directory is deleted if it is empty).

* Replace CLI calls to external tools in virtual environment with API calls to
  external libraries.


0.0.0
=====

2019-05-13

Release initial version.


.. EOF
