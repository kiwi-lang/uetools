import pytest

from uetools.core import args, main
from uetools.core.conf import ready
from uetools.core.testing import git_diff, git_status

skipif = pytest.mark.skipif


#  The multiline break it to force the editor to keep an extra whitespacee
diff = (
    """
diff --git a/Config/DefaultEngine.ini b/Config/DefaultEngine.ini
index 2556b01..35344b6 100644
--- a/Config/DefaultEngine.ini
+++ b/Config/DefaultEngine.ini
@@ -45,3 +45,8 @@ bReportStats=False
 ConnectionType=USBOnly
 bUseManualIPAddress=False
 ManualIPAddress="""
    + """
+[/Script/PythonScriptPlugin.PythonScriptPluginUserSettings]
+bDeveloperMode=True
+bEnableContentBrowserIntegration=True
+[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
+bDeveloperMode=True
"""
)


@skipif(not ready(), reason="Unreal engine is not installed")
def test_python(project, project_name):

    main(args("project", "python", project_name))

    assert "Config/DefaultEngine.ini" in git_status(project)
    assert git_diff(project).strip() == diff.strip()
