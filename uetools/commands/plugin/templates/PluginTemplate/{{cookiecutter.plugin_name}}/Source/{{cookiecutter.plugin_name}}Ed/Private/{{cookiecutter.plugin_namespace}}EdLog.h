// {{cookiecutter.copyright}}

#pragma once

#include "Stats/Stats.h"

DECLARE_LOG_CATEGORY_EXTERN(Log{{cookiecutter.plugin_namespace}}Ed, Log, All);

#define GK{{cookiecutter.plugin_namespace}}_FATAL(Format, ...)   UE_LOG(Log{{cookiecutter.plugin_namespace}}Ed, Fatal, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_ERROR(Format, ...)   UE_LOG(Log{{cookiecutter.plugin_namespace}}Ed, Error, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_WARNING(Format, ...) UE_LOG(Log{{cookiecutter.plugin_namespace}}Ed, Warning, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_DISPLAY(Format, ...) UE_LOG(Log{{cookiecutter.plugin_namespace}}Ed, Display, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_LOG(Format, ...)     UE_LOG(Log{{cookiecutter.plugin_namespace}}Ed, Log, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_VERBOSE(Format, ...) UE_LOG(Log{{cookiecutter.plugin_namespace}}Ed, Verbose, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_VERYVERBOSE(Format, ...) UE_LOG(Log{{cookiecutter.plugin_namespace}}Ed, VeryVerbose, Format, ##__VA_ARGS__)

DECLARE_STATS_GROUP(TEXT("{{cookiecutter.plugin_name}}Ed"), STATGROUP_{{cookiecutter.plugin_namespace}}Ed, STATCAT_Advanced);
