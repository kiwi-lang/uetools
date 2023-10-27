import pytest

from uetools.core.cli import args, main

commands = [
    ("run", ["FakeMap", "--tests", "FakeTest"]),
]

params = []
for cmd, extra in commands:
    # FIXME: this does not return 1
    for rc in (0,):
        params.append((cmd, rc, extra))


@pytest.mark.parametrize("cmd,rc,extra", params)
def test_mock_test(project, project_name, monkeypatch, cmd, rc, extra):
    monkeypatch.setattr(f"uetools.commands.test.{cmd}.popen_with_format", lambda *a, **b: rc)
    assert main(args("test", cmd, "--project", project_name, *extra)) == rc
