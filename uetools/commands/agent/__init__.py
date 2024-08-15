from argklass.command import ParentCommand

import uetools.commands.engine


class Agent(ParentCommand):
    """Set of commands to manage engine installation/source"""

    name: str = "agent"

    @staticmethod
    def module():
        return uetools.commands.agent


COMMANDS = Agent
