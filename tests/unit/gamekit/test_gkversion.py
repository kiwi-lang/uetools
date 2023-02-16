import os

from uetools.core import args, main


def test_gk_version(project, project_name, monkeypatch):
    build_file = os.path.join(project, "Source/ExampleProject/ExampleProject.Build.cs")

    values = [
        'string EXAMPLEPROJECT_TAG = "v0.0.0";',
        'string EXAMPLEPROJECT_HASH = "5e6fafed8a73807d5e067a109d0ba36272dec976";',
        'string EXAMPLEPROJECT_DATE = "2023-02-16 17:53:58 -0500";',
    ]

    with open(build_file) as file:
        data = file.read()

    for v in values:
        assert v not in data

    assert (
        main(
            args(
                "gamekit",
                "gitversion",
                "--namespace",
                "EXAMPLEPROJECT",
                "--file",
                build_file,
            )
        )
        == 0
    )

    with open(build_file) as file:
        data = file.read()

    for v in values:
        assert v in data
