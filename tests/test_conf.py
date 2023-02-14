import os
import shutil
from contextlib import contextmanager

import pytest

from uetools.core.conf import find_project

skipif = pytest.mark.skipif


@contextmanager
def fake_project(path, name):
    project = os.path.join(path, name)
    os.makedirs(project, exist_ok=True)
    uproject = os.path.join(project, f"{name}.uproject")

    with open(uproject, "w", encoding="utf-8") as file:
        file.write("{}")

    yield

    shutil.rmtree(project)


def test_find_project(project_root, project, project_name):

    target = os.path.abspath(
        os.path.join(project_root, project_name, f"{project_name}.uproject")
    )

    assert find_project(project_name) == target
    assert find_project(target) == target, "Accept absolute path"

    # project name is extracted from target
    assert find_project(f"{project_name}Editor") == target
    assert find_project(f"{project_name}tServer") == target


def test_find_project_engine(engine_test_root):

    target = os.path.abspath(
        os.path.join(engine_test_root, "RootProject", "RootProject.uproject")
    )

    with fake_project(engine_test_root, "RootProject"):
        assert find_project("RootProject") == target
