// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class {{cookiecutter.project_name}}EditorTarget : TargetRules
{
	public {{cookiecutter.project_name}}EditorTarget( TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.V2;
		ExtraModuleNames.AddRange( new string[] { "{{cookiecutter.project_name}}" } );
	}
}
