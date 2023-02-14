import json
import os
import subprocess

import pytest

from uetools.core import args, main
from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(os.name == "nt", reason="This does not run on my machine because of bs4")
@skipif(is_ci(), reason="Unreal engine is not installed")
def test_docs(project, project_name, tmp_path):

    assert os.path.exists(os.path.join(project, "Docs")) is False

    path = os.path.join(tmp_path, "config.json")

    with open(path, "w", encoding="utf-8") as config:
        json.dump(
            {
                "default_context": {
                    "project_name": "ExampleProject",
                    "author": "uetools",
                    "email": "My@Email.com",
                    "copyright": "2022",
                    "directory_name": "Docs",
                }
            },
            config,
        )

    main(args("project", "docs", project_name, "--config", path, "--no-input"))

    docs = os.path.join(project, "Docs")
    assert os.path.exists(docs) is True

    subprocess.run(
        "python -m pip install -r requirements.txt".split(" "), cwd=docs, check=True
    )

    # Make sure everything was installed correctly
    # from bs4 import BeautifulSoup
    # _ = BeautifulSoup("", "lxml-xml")

    os.environ["READTHEDOCS"] = "True"

    output = subprocess.run(
        "sphinx-build --color -c . -b html . _build/html".split(" "),
        cwd=docs,
        stderr=subprocess.STDOUT,
        text="utf-8",
    )

    assert output.returncode == 0
