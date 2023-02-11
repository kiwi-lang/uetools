import os
import shutil
from contextlib import contextmanager

import pytest

from uetools.core.conf import engine_root, find_project, project_folder, ready

skipif = pytest.mark.skipif


@contextmanager
def fake_project(path, name):
    project = os.path.join(path, name)
    os.makedirs(project, exist_ok=True)
    uproject = os.path.join(project, f"{name}.uproject")

    with open(uproject, "w", encoding="utf-8") as file:
        pass

    yield

    shutil.rmtree(project)


@skipif(not ready(), reason="Unreal engine is installed")
def test_find_project():

    project = project_folder()[0]
    target = os.path.join(project, "ExampleProject", "ExampleProject.uproject")

    assert find_project("ExampleProject") == target
    assert find_project(target) == target, "Accept absolute path"

    # project name is extracted from target
    assert find_project("ExampleProjectEditor") == target
    assert find_project("ExampleProjectServer") == target


@skipif(not ready(), reason="Unreal engine is installed")
def test_find_project_engine():

    engine = engine_root()
    target = os.path.join(engine, "RootProject", "RootProject.uproject")

    with fake_project(engine, "RootProject"):
        assert find_project("RootProject") == target
