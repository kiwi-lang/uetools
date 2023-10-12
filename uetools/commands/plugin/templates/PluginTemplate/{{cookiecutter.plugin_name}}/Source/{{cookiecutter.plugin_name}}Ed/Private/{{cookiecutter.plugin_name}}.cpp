// Copyright 2023 Mischievous Game, Inc. All Rights Reserved.

#include "{{cookiecutter.plugin_name}}Ed.h"

// Unreal Engine
#include "Engine/Blueprint.h"
#include "Misc/Paths.h"
#include "Modules/ModuleManager.h"


#define LOCTEXT_NAMESPACE "F{{cookiecutter.plugin_name}}EdModule"



void F{{cookiecutter.plugin_name}}EdModule::StartupModule()
{
}

void F{{cookiecutter.plugin_name}}EdModule::ShutdownModule()
{
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(F{{cookiecutter.plugin_name}}EdModule, {{cookiecutter.plugin_name}}Ed)