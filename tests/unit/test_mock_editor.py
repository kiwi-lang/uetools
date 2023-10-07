import pytest

from uetools.core.cli import args, main
from uetools.core.conf import is_ci

skipif = pytest.mark.skipif


@skipif(is_ci(), reason="Unreal engine is not installed")
def test_client(project):
    # the problem is the client just "opens"
    pass


commands = [
    ("client", []),
    ("cook", []),
    ("editor", []),
    ("localize", []),
    ("localize", ["--bootstrap"]),
    ("open", []),
    ("resavepackages", []),
    ("server", ["FakeMap"]),
    ("worldpartition", ["FakeMap"]),
]

params = []
for cmd, extra in commands:
    for rc in (0, 1):
        params.append((cmd, rc, extra))


@pytest.mark.parametrize("cmd,rc,extra", params)
def test_mock_editor(project, project_name, monkeypatch, cmd, rc, extra):
    monkeypatch.setattr(
        f"uetools.commands.editor.{cmd}.popen_with_format", lambda *a, **b: rc
    )
    assert main(args("editor", cmd, "--project", project_name, *extra)) == rc


# def test_mock_editor_ml(project, project_name, monkeypatch, cmd, rc, extra):
#    assert main(args("editor", 'ml', project_name, "FakeMap")) == rc
