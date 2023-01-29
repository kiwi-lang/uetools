"""Argument formatting experimentation"""
from __future__ import annotations

from argparse import Action, _SubParsersAction
from dataclasses import dataclass, field
from functools import singledispatch


class BaseArgumentHelpFormatter:
    def _format_args(self, action, default_metavar):
        # print("_format_args", args, kwargs)
        return ""

    def add_usage(self, usage, actions, groups, prefix=None):
        print("add_usage", usage, actions, groups, prefix)
        return ""

    def format_help(self):
        print("format_help")
        return ""

    # Argument groups
    # start_section
    #  add_text
    #  add_arguments
    # end_section

    def start_section(self, heading: str) -> None:
        print("start_section", heading)
        return ""

    def add_text(self, text: str) -> None:
        print("add_text", text)
        return ""

    def add_arguments(self, actions: list[Action]) -> None:
        print("add_arguments", actions)
        return ""

    def end_section(self) -> None:
        print("end_section")
        return ""


@singledispatch
def format_action(action, level):
    return repr(action)


def _(action: _SubParsersAction):

    frags = []

    for name, _ in action.choices.items():
        helpstr = ""
        frags.append((name, helpstr))

    return


@dataclass
class ArgumentSection:
    name: str = None
    description: str = None
    actions: list[Action] = field(default_factory=list)
    level: int = 0

    def __repr__(self):
        idt = "  "
        idt1 = idt * self.level
        frags = [
            f"{idt1}{self.name}: {self.description}",
        ] + [f"{idt1}{idt}{a}" for a in self.actions]

        return "\n".join(frags)


class ArgumentHelpFormatter(BaseArgumentHelpFormatter):
    def __init__(self):
        self.sections = []
        self.generated = []

    def _format_args(self, action, default_metavar):
        # print("_format_args", args, kwargs)
        return

    def add_usage(self, usage, actions, groups, prefix=None):
        print("add_usage", usage, actions, groups, prefix)
        return ""

    def format_help(self):
        print("format_help")
        frags = []
        for g in self.generated:
            frags.append(repr(g))

        return "\n\n".join(frags)

    def start_section(self, heading: str) -> None:
        self.sections.append(ArgumentSection(name=heading, level=len(self.sections)))

    def add_text(self, text: str) -> None:
        if self.sections:
            self.sections[-1].description = text

    def add_arguments(self, actions: list[Action]) -> None:
        if self.sections:
            self.sections[-1].actions = actions

    def end_section(self) -> None:
        if self.sections:
            self.generated.append(self.sections.pop())
