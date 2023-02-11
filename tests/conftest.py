import os
import shutil
import subprocess

import pytest

from uetools.core.conf import load_conf

original_name = "ExampleProject"
clean_project = "https://github.com/kiwi-lang/ExampleProject"

PROJECT_PATHS = load_conf().get("project_path")
PROJECT_ROOT = PROJECT_PATHS[0] if PROJECT_PATHS else None
HAS_UNREAL_ENGINE = PROJECT_ROOT is not None


# Because fixtures are cached per test we can add any of the child fixture to get the data
# we need


@pytest.fixture
def project_root():
    return PROJECT_ROOT


@pytest.fixture
def project_name(project_root):
    # i = 0
    # name = f"MyProjectT{i}"
    # while os.path.exists(os.path.join(PROJECT_ROOT, name)):
    #     i += 1
    #     name = f"MyProjectT{i}"

    return original_name


@pytest.fixture
def project(project_name, project_root):
    """Create a new empty project to test commands"""

    path = os.path.join(PROJECT_ROOT, project_name)
    original = os.path.join(project_root, original_name)

    # if the original projet does not exist yet, copy it
    if not os.path.exists(original):
        subprocess.run(
            ["git", "clone", clean_project, original],
            check=True,
        )

    # Instead of copying and deleting the folder just rely on git
    # to clean everything
    subprocess.run(["git", "reset", "--hard"], cwd=original)

    try:
        subprocess.run(["git", "rm", "Plugins/ExamplePlugin2"], cwd=original)
        shutil.rmtree(os.path.join(original, "Plugins/ExamplePlugin2"))
    except:
        pass

    # remoes files, directory and ignored files
    subprocess.run(["git", "clean", "-fdx"], cwd=original)

    yield path

    # Leave the repo as is for debugging
