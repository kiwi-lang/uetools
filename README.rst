Unreal Engine Tools
===================

|pypi| |py_versions| |codecov| |docs| |tests| |style|

.. |pypi| image:: https://img.shields.io/pypi/v/uetools.svg
    :target: https://pypi.python.org/pypi/uetools
    :alt: Current PyPi Version

.. |py_versions| image:: https://img.shields.io/pypi/pyversions/uetools.svg
    :target: https://pypi.python.org/pypi/uetools
    :alt: Supported Python Versions

.. |codecov| image:: https://codecov.io/gh/kiwi-lang/uetools/branch/master/graph/badge.svg?token=40Cr8V87HI
   :target: https://codecov.io/gh/kiwi-lang/uetools

.. |docs| image:: https://readthedocs.org/projects/uetools/badge/?version=latest
   :target:  https://uetools.readthedocs.io/en/latest/?badge=latest

.. |tests| image:: https://github.com/kiwi-lang/uetools/actions/workflows/test.yml/badge.svg?branch=master
   :target: https://github.com/kiwi-lang/uetools/actions/workflows/test.yml

.. |style| image:: https://github.com/kiwi-lang/uetools/actions/workflows/style.yml/badge.svg?branch=master
   :target: https://github.com/kiwi-lang/uetools/actions/workflows/style.yml



``uetools`` implements a set of tools to make it easier to work with Unreal Engine projects and automate common tasks.

Get Started
-----------

.. code-block::

   pip install uetools

   # Saves common paths
   uecli init --engine C:/opt/UnrealEngine/Engine --projects C:/opt/Projects

   # Install the plugin VoxelPlugin to the RTSGame project
   uecli install RTSGame https://github.com/Phyronnaz/VoxelPlugin

   # Rebuild the RTSGame project
   uecli build RTSGame

   # Open the project (located in C:/opt/Projects/RTSGame)
   uecli open RTSGame

   # Cook the project
   uecli cook RTSGame

   # Start a server
   uecli server RTSGame --dedicated --port 8123

   # start a client
   uecli client RTSGame --address 127.0.0.1 --port  8123


Features
--------

* Windows & Linux
* Open projects
* Build
* Run automated tests
* Cook
* Generate localization files for internationalization
* Run the editor

It also implements common recipes such as

* Install project plugins from a repository
* Disable plugins
* Add dedicated server targets
* Automatically configure project settings for Python
* Works on both Linux & Windows seemlessly
* Add Doxygen to your project


Rational
--------

Unreal engine has 222 comandlets, 83 commands and more than 1237 command line parameters hidden inside its code,
very few are documented.

``uetools`` identifies the useful arguments and bundle them inside a command line utility, forming groups/set of arguments
with a singular purpose.
