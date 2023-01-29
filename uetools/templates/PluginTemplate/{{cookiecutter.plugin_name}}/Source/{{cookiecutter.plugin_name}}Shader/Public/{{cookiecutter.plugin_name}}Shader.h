// Copyright 2023 Mischievous Game, Inc. All Rights Reserved.

#pragma once

#include "Modules/ModuleManager.h"
#include "Stats/Stats.h"

/*
DECLARE_LOG_CATEGORY_EXTERN(LogGKFoWShader, Log, All);

#define GKFOGSHD_FATAL(Format, ...)       UE_LOG(LogGKFoWShader, Fatal, Format, ##__VA_ARGS__)
#define GKFOGSHD_ERROR(Format, ...)       UE_LOG(LogGKFoWShader, Error, Format, ##__VA_ARGS__)
#define GKFOGSHD_WARNING(Format, ...)     UE_LOG(LogGKFoWShader, Warning, Format, ##__VA_ARGS__)
#define GKFOGSHD_DISPLAY(Format, ...)     UE_LOG(LogGKFoWShader, Display, Format, ##__VA_ARGS__)
#define GKFOGSHD_LOG(Format, ...)         UE_LOG(LogGKFoWShader, Log, Format, ##__VA_ARGS__)
#define GKFOGSHD_VERBOSE(Format, ...)     UE_LOG(LogGKFoWShader, Verbose, Format, ##__VA_ARGS__)
#define GKFOGSHD_VERYVERBOSE(Format, ...) UE_LOG(LogGKFoWShader, VeryVerbose, Format, ##__VA_ARGS__)

DECLARE_STATS_GROUP(TEXT("{{cookiecutter.plugin_name}}Shader"), STATGROUP_GKFoWShader, STATCAT_Advanced);
*/

class F{{cookiecutter.plugin_name}}ShaderModule: public IModuleInterface
{
    public:
    /** IModuleInterface implementation */
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;
};
