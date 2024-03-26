import pytest

from uetools.core.cli import args, main


@pytest.mark.parametrize("rc", [0, 1])
def test_mock_plugin_pacakge(project, project_name, monkeypatch, rc):
    monkeypatch.setattr("uetools.commands.plugin.package.popen_with_format", lambda *a, **b: rc)
    assert (
        main(
            args(
                "plugin",
                "package",
                "--project",
                project_name,
                "--plugin",
                "Plugins/ExamplePlugin",
                "output"
            )
        )
        == rc
    )
