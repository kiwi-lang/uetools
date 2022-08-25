import json
import os
import subprocess

import pytest

from uetools.core import args, main
from uetools.core.conf import ready

skipif = pytest.mark.skipif


@skipif(not ready(), reason="Unreal engine is not installed")
def test_docs(project, project_name, tmp_path):

    assert os.path.exists(os.path.join(project, "Docs")) is False

    path = os.path.join(tmp_path, "config.json")

    with open(path, "w", encoding="utf-8") as config:
        json.dump(
            {
                "project_name": "ExampleProject",
                "author": "uetools",
                "email": "My@Email.com",
                "copyright": "2022",
                "directory_name": "Docs",
            },
            config,
        )

    main(args("docs", project_name, "--config", path, "--no-input"))

    docs = os.path.join(project, "Docs")
    assert os.path.exists(docs) is True

    subprocess.run("pip install -r requirements.txt".split(" "), cwd=docs, check=True)

    os.environ["READTHEDOCS"] = "True"
    subprocess.run(
        "sphinx-build --color -c . -b html . _build/html".split(" "),
        cwd=docs,
        check=True,
    )
