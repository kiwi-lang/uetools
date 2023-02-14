import pytest

from uetools.core import args, main

commands = [
    ("cook", []),
    ("localize", []),
    ("test", ["FakeTest"]),
]

params = []
for cmd, extra in commands:
    for rc in (0, 1):
        params.append((cmd, rc, extra))


@pytest.mark.parametrize("cmd,rc,extra", params)
def test_mock_uat(project, project_name, monkeypatch, cmd, rc, extra):
    monkeypatch.setattr(
        f"uetools.commands.uat.{cmd}.popen_with_format", lambda *a, **b: rc
    )
    assert main(args("uat", cmd, project_name, *extra)) == rc


@pytest.mark.parametrize("rc", [0, 1])
def test_mock_uat_uat(project, project_name, monkeypatch, rc):
    monkeypatch.setattr(
        "uetools.commands.uat.uat.popen_with_format", lambda *a, **b: rc
    )
    assert main(args("uat", "uat", "RunUnrealTests", project_name)) == rc
