import pytest

from uetools.core.cli import args, main
from uetools.core.testing import git_diff, git_status

skipif = pytest.mark.skipif


# The multiline break it to force the editor to keep an extra whitespacee
diff = """+[/Script/PythonScriptPlugin.PythonScriptPluginUserSettings]
+bDeveloperMode=True
+bEnableContentBrowserIntegration=True
+[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
+bDeveloperMode=True
"""


def test_python(project, project_name):
    # pat = "(.*)" + re.escape(diff).strip() + "\n(.*)"
    # print(pat)
    # regex = re.compile(pat, flags=re.MULTILINE)

    main(args("project", "python", project_name))

    assert "Config/DefaultEngine.ini" in git_status(project)

    actual_diff = git_diff(project).strip()[-len(diff) :]
    assert actual_diff.strip() == diff.strip()
