import pytest

from uetools.core.cli import args, main

commands = [
    ("gkscript", []),
]

params = []
for cmd, extra in commands:
    for rc in (0, 1):
        params.append((cmd, rc, extra))


@pytest.mark.parametrize("cmd,rc,extra", params)
def test_mock_gamekit(project, project_name, monkeypatch, cmd, rc, extra):
    monkeypatch.setattr(
        f"uetools.plugins.gamekit.{cmd}.popen_with_format", lambda *a, **b: rc
    )
    assert main(args("gamekit", cmd, project_name, *extra)) == rc
