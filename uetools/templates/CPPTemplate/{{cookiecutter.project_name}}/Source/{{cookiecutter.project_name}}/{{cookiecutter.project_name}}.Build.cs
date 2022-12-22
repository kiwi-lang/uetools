// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class {{cookiecutter.project_name}} : ModuleRules
{
	public {{cookiecutter.project_name}}(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
	
		PublicDependencyModuleNames.AddRange(new string[] { 
			"Core", 
			"CoreUObject", 
			"Engine", 
			"InputCore" 
		});

		PrivateDependencyModuleNames.AddRange(new string[] {  });

	}
}
