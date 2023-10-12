// {{cookiecutter.copyright}}

#include "{{cookiecutter.plugin_name}}Test.h"

// Unreal Engine
#include "Engine/Blueprint.h"
#include "Misc/Paths.h"
#include "Modules/ModuleManager.h"
#include "ShaderCore.h"

#define LOCTEXT_NAMESPACE "F{{cookiecutter.plugin_name}}TestModule"



void F{{cookiecutter.plugin_name}}TestModule::StartupModule()
{
}

void F{{cookiecutter.plugin_name}}TestModule::ShutdownModule()
{
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(F{{cookiecutter.plugin_name}}TestModule, {{cookiecutter.plugin_name}}Test)