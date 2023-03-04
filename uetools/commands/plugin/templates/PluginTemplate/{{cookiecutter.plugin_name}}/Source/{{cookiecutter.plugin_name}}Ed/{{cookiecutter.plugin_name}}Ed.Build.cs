// Copyright 2023 Mischievous Game, Inc. All Rights Reserved.

using System;
using System.IO;
using UnrealBuildTool;
using System.Diagnostics;
using EpicGames.Core;


public class {{cookiecutter.plugin_name}}Ed : ModuleRules
{
    public {{cookiecutter.plugin_name}}Ed(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicIncludePaths.Add(Path.Combine(ModuleDirectory));

        // ... add other public dependencies that you statically link with here ...
        PublicDependencyModuleNames.AddRange(new string[] {
                "Core",
                "{{cookiecutter.plugin_name}}",
                "{{cookiecutter.plugin_name}}Shader",
        });

        PrivateDependencyModuleNames.AddRange(new string[] {
                "CoreUObject",
                "Engine",
                "Slate",
                "SlateCore",

                "RenderCore",   // Custom Shader
				"AIModule",	    // TeamAgent Interface
				"Landscape",    // Landscape
                "RHI",          // Shader
        });

    }
}
