// BSD 3-Clause License Copyright (c) 2022, Pierre Delaunay All rights reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class {{cookiecutter.project_name}}ServerTarget : TargetRules
{
    public {{cookiecutter.project_name}}ServerTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Server;
        DefaultBuildSettings = BuildSettingsVersion.V2;
        ExtraModuleNames.Add("{{cookiecutter.project_name}}");
    }
}
