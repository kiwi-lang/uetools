Adding new commands
-------------------

You can extend uetools with your own commands.
An example is provided here `plugin example <https://github.com/kiwi-lang/uetools.plugins.myplugin>`_

The example creates a new python package that extends uetools.plugins with its own commands.
Once the package is installed (``pip install -e .`` for a local development install
or ``pip install git+https://github.com/kiwi-lang/uetools.plugins.myplugin`)
you can use your commands by calling ``uecli name-of-your-command ...``.

You will note that ``uetools`` use a dataclass to define the arguments of its commands.
As long as the name of the attribute matches the name of the argument in the underlying command
almost no boilerplate code is needed.


.. code-block:: python

   """My new command"""
   from dataclasses import dataclass

   from simple_parsing import choice
   from uetools.core.command import Command, command_builder
   from uetools.core.conf import editor_cmd, find_project, uat
   from uetootls.run import popen_with_format
   from uetools.format.base import Formatter


   @dataclass
   class Arguments:
      """Arguments for my new command"""

      project: str
      flag: bool = False
      value: str = ""
      choice: str = choice("a", "b", "c", type=str, default="a")


   class MyNewCommand(Command):
      """My new command does this"""

      name: str = "command"

      @staticmethod
      def arguments(subparsers):
         """Add arguments to the parser"""
         parser = subparsers.add_parser(MyNewCommand.name, help="Run my custom command")
         parser.add_arguments(Arguments, dest="args")

      @staticmethod
      def execute(args):
         """Execute the command"""
         cmd = command_builder(args)

         uproject = find_project(args.args.project)

         fmt = Formatter()
         popen_with_format(fmt, [uat(), uproject] + cmd)

         return popen_with_format(fmt, [editor_cmd()] + cmd)

   # Register the commands here
   COMMANDS = [
      MyNewCommand,
   ]
