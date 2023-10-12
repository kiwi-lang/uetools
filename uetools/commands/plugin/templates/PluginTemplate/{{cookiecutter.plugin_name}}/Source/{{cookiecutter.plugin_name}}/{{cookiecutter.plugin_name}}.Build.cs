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

        if (Target.bBuildEditor == true)
        {
            // FEditorDelegates
            PrivateDependencyModuleNames.Add("UnrealEd");
        }

        // Version Info
        // ------------
        // Automatically set by the CI
        string {{cookiecutter.plugin_upper}}_TAG = "v0.0.1";
        string {{cookiecutter.plugin_upper}}_HASH = "NA";
        string {{cookiecutter.plugin_upper}}_DATE = "1970-01-01 00:00:00 +0000";

        PublicDefinitions.Add("{{cookiecutter.plugin_upper}}_TAG=" + {{cookiecutter.plugin_upper}}_TAG);
        PublicDefinitions.Add("{{cookiecutter.plugin_upper}}_COMMIT=" + {{cookiecutter.plugin_upper}}_HASH);
        PublicDefinitions.Add("{{cookiecutter.plugin_upper}}_DATE=" + {{cookiecutter.plugin_upper}}_DATE);
    }
}
