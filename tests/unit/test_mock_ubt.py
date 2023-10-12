import pytest

from uetools.core.cli import args, main

commands = [
    ("ubt", []),
    ("build", []),
    ("build", ["--profile", "update-project"]),
]

params = []
for cmd, extra in commands:
    for rc in (0, 1):
        params.append((cmd, rc, extra))


@pytest.mark.parametrize("cmd,rc,extra", params)
def test_mock_ubt(project, project_name, engine_test_root, monkeypatch, cmd, rc, extra):
    monkeypatch.setattr(
        f"uetools.commands.ubt.{cmd}.popen_with_format", lambda *a, **b: rc
    )
    monkeypatch.setattr(
        "uetools.commands.ubt.build.engine_folder", lambda: engine_test_root
    )

    if rc == 0:
        assert main(args("ubt", cmd, project_name, *extra)) == rc
    else:
        assert main(args("ubt", cmd, project_name, *extra)) in (rc, rc * 6)


@pytest.mark.parametrize("rc", [0, 1])
def test_mock_ubt_regen(project, project_name, monkeypatch, rc):
    monkeypatch.setattr(
        "uetools.commands.ubt.regenerate.popen_with_format", lambda *a, **b: rc
    )

    if rc == 0:
        assert main(args("ubt", "regenerate", "--project", project_name)) == rc
    else:
        assert main(args("ubt", "regenerate", "--project", project_name)) in (
            rc,
            rc * 6,
        )


def test_mock_ubt_config(project, project_name):
    rc = 0
    assert main(args("ubt", "configure", "--list")) == rc
