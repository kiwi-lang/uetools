// Copyright 2023 Mischievous Game, Inc. All Rights Reserved.

using System.IO;
using UnrealBuildTool;

public class {{cookiecutter.plugin_name}}Shader : ModuleRules
{
    public {{cookiecutter.plugin_name}}Shader(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicIncludePaths.Add(Path.Combine(ModuleDirectory));

        PublicDependencyModuleNames.AddRange(new string[] {
            "Core",

        });

        PrivateDependencyModuleNames.AddRange(new string[] {
            "CoreUObject",
            "Engine",
            "Slate",
            "SlateCore",

            "RenderCore", // Custom Shader
            "RHI"         // Shader
        });
    }
}
