..


.. Keep the current version number on line number 5
0.0.7
=====

2020-04-21

* Replace CLI optional '--tools' with positional


0.0.6
=====

2020-04-20

* Add support for 'requirements.txt' files
* Fix call to main entry point of 'shiv', somewhat revert the change introduced
  in version '0.0.5'.
* Show summary in CLI's help output
* Add test against Python3.8 in Travis CI and GitLab


0.0.5
=====

2020-03-30

* Update 'zapp' to version '0.0.6'
* Fix call to main entry point of 'shiv'
* Add help messages for CLI options


0.0.4
=====

2020-01-09

* Rewrite naming scheme for output files


0.0.3
=====

2019-09-30

* Add support for ``tools_directory`` setting

* Use operating system's standard value for default location of the
  configuration file


0.0.2
=====

2019-09-18

* Add namespaces in configuration file

* Add support for default settings

* Change interpolation in configuration files

* Add support for Windows specific output file name


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
