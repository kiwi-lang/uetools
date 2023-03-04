// Copyright 2023 Mischievous Game, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Stats/Stats.h"
#include "Modules/ModuleManager.h"


/*
DECLARE_LOG_CATEGORY_EXTERN(LogGKFoW, Log, All);

#define GKFOG_FATAL(Format, ...)   UE_LOG(LogGKFoW, Fatal, Format, ##__VA_ARGS__)
#define GKFOG_ERROR(Format, ...)   UE_LOG(LogGKFoW, Error, Format, ##__VA_ARGS__)
#define GKFOG_WARNING(Format, ...) UE_LOG(LogGKFoW, Warning, Format, ##__VA_ARGS__)
#define GKFOG_DISPLAY(Format, ...) UE_LOG(LogGKFoW, Display, Format, ##__VA_ARGS__)
#define GKFOG_LOG(Format, ...)     UE_LOG(LogGKFoW, Log, Format, ##__VA_ARGS__)
#define GKFOG_VERBOSE(Format, ...) UE_LOG(LogGKFoW, Verbose, Format, ##__VA_ARGS__)
#define GKFOG_VERYVERBOSE(Format, ...) UE_LOG(LogGKFoW, VeryVerbose, Format, ##__VA_ARGS__)

DECLARE_STATS_GROUP(TEXT("{{cookiecutter.plugin_name}}"), STATGROUP_GKFoW, STATCAT_Advanced);
*/

class F{{cookiecutter.plugin_name}}EdModule : public IModuleInterface
{
public:

	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
