import pytest

from uetools.core.cli import args, main


@pytest.mark.parametrize("rc",  (0, 1))
def test_mock_ubt(project, project_name, engine_test_root, monkeypatch, rc):
    monkeypatch.setattr("uetools.commands.ubt.ubt.popen_with_format", lambda *a, **b: rc)
    monkeypatch.setattr("uetools.commands.ubt.build.engine_folder", lambda: engine_test_root)

    if rc == 0:
        assert main(args("ubt", "ubt", "--project", project_name, "TargetNane")) == rc
    else:
        assert main(args("ubt", "ubt", "--project", project_name, "TargetNane")) in (rc, rc * 6)


@pytest.mark.parametrize("rc",  (0, 1))
def test_mock_ubt_build(project, project_name, engine_test_root, monkeypatch, rc):
    monkeypatch.setattr("uetools.commands.ubt.build.popen_with_format", lambda *a, **b: rc)
    monkeypatch.setattr("uetools.commands.ubt.build.engine_folder", lambda: engine_test_root)

    if rc == 0:
        assert main(args("ubt", "build", project_name)) == rc
    else:
        assert main(args("ubt", "build", project_name)) in (rc, rc * 6)

@pytest.mark.parametrize("rc",  (0, 1))
def test_mock_ubt_build_profile(project, project_name, engine_test_root, monkeypatch, rc):
    monkeypatch.setattr("uetools.commands.ubt.build.popen_with_format", lambda *a, **b: rc)
    monkeypatch.setattr("uetools.commands.ubt.build.engine_folder", lambda: engine_test_root)

    if rc == 0:
        assert main(args("ubt", "build", "--profile", "update-project", project_name)) == rc
    else:
        assert main(args("ubt", "build", "--profile", "update-project", project_name)) in (rc, rc * 6)


@pytest.mark.parametrize("rc", [0, 1])
def test_mock_ubt_regen(project, project_name, monkeypatch, rc):
    monkeypatch.setattr("uetools.commands.ubt.regenerate.popen_with_format", lambda *a, **b: rc)

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
