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



``uetools`` implements a set of tools to make it easier to work
with Unreal Engine projects and automate common tasks.

Get Started
-----------

.. code-block:: bash

   pip install uetools

   # Saves common paths
   uecli init --engine C:/opt/UnrealEngine/Engine --projects C:/opt/Projects
   uecli engine add --version src --engine C:/opt/UnrealEngine/Engine
   uecli engine add --version 5.1 --engine C:/EpicGames/UE_5.1/Engine
   uecli engine add --version 5.0 --engine C:/EpicGames/UE_5.0/Engine

   # Install the plugin VoxelPlugin to the RTSGame project
   uecli plugin install RTSGame https://github.com/Phyronnaz/VoxelPlugin

   # Rebuild the RTSGame project
   uecli ubt build RTSGame

   # Open the project (located in C:/opt/Projects/RTSGame)
   uecli editor open RTSGame
   uecli -v 5.1 editor open RTSGame
   uecli -v 5.0 editor open RTSGame

   # Cook the project
   uecli editor cook RTSGame

   # Start a server
   uecli editor server RTSGame --dedicated --port 8123

   # start a client
   uecli editor client RTSGame --address 127.0.0.1 --port  8123

   # Turn a blueprint Project into a C++ project
   uecli project cpp RTSGame


Make your own command
---------------------

You can extend uetoosl for your organization by creating plugins.
A `template <https://github.com/kiwi-lang/uetools.plugins.myplugin>`_ is provided to help you get started.


Help Example
------------

.. code-block:: bash

   Pattern:
      uecli [-v version] command subcommand ...

   Examples:
      uecli -v 5.1 editor open RTSGame --help


   positional arguments
      project: str                             Name of the the project to open
      map: str                                 Name of the map to open

   optional arguments
      --dry: bool = False                      Print the command it will execute without running it

   Arguments
      --resx: int = 320                        resolution width
      --resy: int = 240                        resolution height
      --fps: int = 20                          Max FPS
      --windowed = True                        Window mode
      --usefixedtimestep = True                Block until the ML agent replies with an action
      --game = True
      --unattended = True                      Close when the game finishes
      --onethread: bool = False                Run on a single thread
      --reducethreadusage: bool = False
      --nosound: bool = False                  Disable sound
      --nullrhi: bool = False                  Disable rendering
      --deterministic: bool = False            Set seeds ?
      --debug: bool = False
      --mladapterport: int = 8123              RPC server listen port


Features
--------

* Windows & Linux
* Open projects
* Build
* Run automated tests
* Cook
* Generate localization files for internationalization
* Run the editor
* multi version support

It also implements common recipes such as

* Install project plugins from a repository
* Disable plugins
* Add dedicated server targets
* Automatically configure project settings for Python
* Works on both Linux & Windows seamlessly
* Add Doxygen to your project


Rational
--------

Unreal engine has 222 comandlets, 83 commands and more than
1237 command line parameters hidden inside its code, very few are documented.

``uetools`` identifies the useful arguments and bundle them inside a command line utility,
forming groups/set of arguments with a singular purpose.


Commands
--------

.. code-block:: bash

      editor                                   Set of commands to launch the editors in different modes
         client                                   Launch the editor as a client to an already running server
         cook                                     Cook your main game
         run                                      Runs Editor as is. This command exposes a lot of arguments.
         localize                                 Generate localization files using unreal editor
         ml                                       Launch a game setup for machine learning
         open                                     Open the editor for a given project
         resavepackages                           Resave assets, fixing some issues that can arise when using marketplace assets
         server                                   Launch the editor as a server
      engine                                   Set of commands to manage engine installation/source
         update                                   Update the engine source code
      format                                   Format UnrealEngine log output. It will attempt to align log output to make them more easily readable.
      init                                     Initialize the configuration file for the command line interface
      plugin                                   Set of commands to create, package and publish plugins
         disable                                  Disable unused plugin that are loading by default
         finalize                                 Finalize Plugin for redistribution
         install                                  Install a plugin to an unreal project.
         list                                     List installed plugin
         new                                      Create a new plugin from a template
         package                                  Builds and cook a plugin
      project                                  Set of commands to manage an UnrealProject
         cpp                                      Turn a blueprint project into a C++ project
         new                                      WIP Create a new project
         dedicated                                Create a dedicated server target for a given project
         docs                                     Add a docs folder to your project
         python                                   Tweak your project settings to enable python scripting in your project
         vscode                                   Tweak your VSCode setting for this project to find python stub generated by Unreal Engine.
      test                                     Set of commands to run automated tests
         run                                      Execute automated tests for a given project
      uat                                      Unreal Automation Tool Commands
         cook                                     Cook your main game using UAT
         localize                                 Use the UAT to run localization gathering
         test                                     Execute automated tests for a given project using UAT
         uat                                      Runs Unreal Automation tool.
      ubt                                      Unreal Build Tool Commands
         build                                    Execute UnrealBuildTool for a specified target
         configure                                Disable unused plugin that are loading by default
         regenerate                               Generate project files
         ubt                                      Runs Unreal build tool as is.
      asset-dumper                             Dump a UAsset
      gamekit                                  Set of commands for Gamekit
         gkscript                                 Convert a Blueprint into GKScript
         gitversion                               Update a file with git version info
