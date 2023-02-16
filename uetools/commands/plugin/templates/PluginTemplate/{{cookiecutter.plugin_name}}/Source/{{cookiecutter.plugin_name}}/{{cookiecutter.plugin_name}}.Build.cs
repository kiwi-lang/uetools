// Copyright 2023 Mischievous Game, Inc. All Rights Reserved.

using System;
using System.IO;
using UnrealBuildTool;
using System.Diagnostics;
using EpicGames.Core;


public class {{cookiecutter.plugin_name}} : ModuleRules
{
    public {{cookiecutter.plugin_name}}(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicIncludePaths.Add(Path.Combine(ModuleDirectory));

        // ... add other public dependencies that you statically link with here ...
        PublicDependencyModuleNames.AddRange(new string[] {
                "Core",
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

        // Version Info
        // ------------
        // Automatically set by the CI
        string {{cookiecutter.plugin_name}}_TAG = "v1.2.0";
        string {{cookiecutter.plugin_name}}_HASH = "fd5965b0a334ba5784929aac36716dbf0e9fb9fb";
        string {{cookiecutter.plugin_name}}_DATE = "2023-01-15 03:23:34 +0000";

        PublicDefinitions.Add("{{cookiecutter.plugin_name}}_TAG=" + {{cookiecutter.plugin_name}}_TAG);
        PublicDefinitions.Add("{{cookiecutter.plugin_name}}_COMMIT=" + {{cookiecutter.plugin_name}}_HASH);
        PublicDefinitions.Add("{{cookiecutter.plugin_name}}_DATE=" + {{cookiecutter.plugin_name}}_DATE);
    }
}
