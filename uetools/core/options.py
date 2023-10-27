import dataclasses
import os

from argklass.arguments import choice

from uetools.core.conf import get_build_modes, get_build_platforms, guess_platform
from uetools.core.util import deduce_plugin, deduce_project


def platform_choice():
    return choice(*get_build_platforms(), default=guess_platform())


def platform_choices():
    metadata = dict()
    metadata["nargs"] = "+"
    metadata["choices"] = get_build_platforms()
    metadata["_kind"] = "argument"
    metadata["type"] = str
    metadata["default"] = [guess_platform()]

    return dataclasses.field(default_factory=lambda: [guess_platform()], metadata=metadata)


def build_mode_choice():
    metadata = dict()
    metadata["choices"] = get_build_modes()
    metadata["_kind"] = "argument"
    metadata["type"] = str

    return dataclasses.field(default=None, metadata=metadata)


def deduce_targets():
    # path to the uproject
    project = deduce_project()

    if project is None:
        return []

    project_name = os.path.basename(project)[: -len(".uproject")]
    project_folder = os.path.join(os.path.dirname(project), "Source")

    targets = [project_name]
    for files in os.listdir(project_folder):
        if files.endswith(".Target.cs"):
            target = files[: -len(".Target.cs")]

            if target not in targets:
                targets.append(target)

    return targets


def pluginfield():
    value = deduce_plugin()

    metadata = dict()
    metadata["_kind"] = "argument"
    metadata["type"] = str

    if value is not None:
        metadata["default"] = value
    else:
        metadata["required"] = True

    return dataclasses.field(default=value, metadata=metadata)


def projectfield():
    value = deduce_project()

    metadata = dict()
    metadata["_kind"] = "argument"
    metadata["type"] = str

    if value is not None:
        metadata["default"] = value
    else:
        metadata["required"] = True

    return dataclasses.field(default=value, metadata=metadata)


def target_choice():
    targets = deduce_targets()

    metadata = dict()
    metadata["_kind"] = "argument"
    metadata["type"] = str

    if len(targets) > 0:
        metadata["choices"] = targets
        metadata["default"] = targets[0]
        return dataclasses.field(default=targets[0], metadata=metadata)

    return dataclasses.field(default=None, metadata=metadata)
