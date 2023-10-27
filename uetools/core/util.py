from __future__ import annotations

import os
from contextlib import contextmanager
import re
from argparse import Namespace
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from functools import lru_cache
from pathlib import Path
import time
import threading

from uetools.core.perf import timeit

_re_deduce_project_plugin = re.compile(r"(.*)(\\|/)(?P<Project>([A-Za-z0-9]*))(\\|/)Plugins(\\|/)(?P<Plugin>([A-Za-z0-9]*))(.*)")


def find_file_like(path, pat):
    path = Path(path)

    while path:
        results = list(path.glob(pat))

        if results:
            return results[0], path

        if path == path.parent:
            break

        path = path.parent

    return None, path


@lru_cache(maxsize=None)
def deduce_project_plugin(path=os.getcwd()):
    path = str(path)

    result = _re_deduce_project_plugin.search(path)
    if result:
        data = result.groupdict()
        plugin_path = os.path.join(path, f"{data['Plugin']}.uplugin")
        return data["Project"], plugin_path

    # Iteratively go up the tree looking for the plugin
    plugin, remain = find_file_like(path, "*.uplugin")
    project = deduce_project(path)
    return project, plugin


def deduce_plugin(path=os.getcwd()):
    _, plugin = deduce_project_plugin(path)
    return str(plugin)


@lru_cache(maxsize=None)
def deduce_project_absolute(path=os.getcwd()):
    result, remain = find_file_like(path, "*.uproject")
    if result:
        return result
    return None


def deduce_project(path=os.getcwd()) -> Path:
    result = deduce_project_absolute(path)
    if result:
        return str(result)
    return None


def deduce_project_folder(path=os.getcwd()):
    result = deduce_project_absolute(path)
    if result:
        return str(result.parent.name)
    return None


@lru_cache(maxsize=None)
def deduce_module(path=os.getcwd()):
    path, remain = find_file_like(path, "*Build..cs")
    return str(os.path.dirname(path))


def command_builder(args: dict | Namespace, ignore=None) -> list[str]:
    """Convert a namespace of arguments into a list of command line arguments for unreal engine.
    Supports dataclasses (even nested) and custom command generation through the ``to_ue_cmd`` method.

    Examples
    --------
    >>> from dataclasses import dataclass

    >>> command_builder(dict(log=True, map='/Game/Map/TopDown'))
    ['-log', '-map=/Game/Map/TopDown']

    >>> @dataclass
    ... class Arguments:
    ...     flag       : bool = False
    ...     goalscore  : Optional[float] = None
    ...     something  : Optional[str] = None

    >>> command_builder(dict(vector=Arguments(flag=True, goalscore=2, something=None)))
    ['-flag', '-goalscore=2']

    >>> command_builder(dict(vector=Arguments(flag=False, goalscore=2)))
    ['-goalscore=2']


    >>> @dataclass
    ... class Vector:
    ...     x: Optional[float] = 0
    ...     y: Optional[float] = 0
    ...     z: Optional[float] = 0
    ...     def to_ue_cmd(self, name, cmd):
    ...         cmd.append(f"-{name}=(X={self.x},Y={self.y},Z={self.z})")

    >>> command_builder(dict(vector=Vector(x=1, y=2, z=3)))
    ['-vector=(X=1,Y=2,Z=3)']

    >>> command_builder(Namespace(vector=Vector(x=1, y=2, z=3)))
    ['-vector=(X=1,Y=2,Z=3)']

    """

    with timeit("command_builder"):
        if ignore is None:
            ignore = set()

        args = deepcopy(args)

        if isinstance(args, Namespace):
            args = vars(args)

        if not isinstance(args, dict):
            args = asdict(args)

        # Note: we do not NEED to pop them, UE ignore unknown arguments
        if isinstance(args, dict):
            args.pop("command", None)
            args.pop("cli", None)
            args.pop("dry", None)

        cmd = []

        _command_builder(cmd, args, ignore)

    return cmd


def _command_builder(cmd, args, ignore):
    for k, v in args.items():
        if v is None:
            continue

        if k in ignore:
            continue

        if isinstance(v, bool):
            if v is not None and v is True:
                cmd.append(f"-{k}")

        elif isinstance(v, (str, int)):
            cmd.append(f"-{k}={v}")

        elif hasattr(v, "to_ue_cmd"):
            v.to_ue_cmd(k, cmd)

        elif is_dataclass(v):
            _command_builder(cmd, asdict(v), ignore)






def _tailf(filename, condition):
    while not os.path.exists(filename):
        pass

    try:
        with open(filename, 'r') as fp:
            while not condition.is_set():
                line = fp.readline()

                if line:
                    print(line, end='')
                
                else:
                    time.sleep(0.1)

    except Exception as err:
        print(err)


@contextmanager
def tailf(filename):
    condition = threading.Event()
    showlog = threading.Thread(
        target=_tailf, 
        args=(filename, condition)
    )
    showlog.start()
    # condition.wait()
    # condition.clear()

    yield 

    condition.set()
    showlog.join()
    

if __name__ == "__main__":
    print(deduce_project_plugin(os.getcwd()))
    print(deduce_project(os.getcwd()))
