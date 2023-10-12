// {{cookiecutter.copyright}}

#pragma once

#include "Stats/Stats.h"


DECLARE_LOG_CATEGORY_EXTERN(Log{{cookiecutter.plugin_namespace}}Shader, Log, All);

#define GK{{cookiecutter.plugin_namespace}}_FATAL(Format, ...)   UE_LOG(Log{{cookiecutter.plugin_namespace}}Shader, Fatal, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_ERROR(Format, ...)   UE_LOG(Log{{cookiecutter.plugin_namespace}}Shader, Error, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_WARNING(Format, ...) UE_LOG(Log{{cookiecutter.plugin_namespace}}Shader, Warning, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_DISPLAY(Format, ...) UE_LOG(Log{{cookiecutter.plugin_namespace}}Shader, Display, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_LOG(Format, ...)     UE_LOG(Log{{cookiecutter.plugin_namespace}}Shader, Log, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_VERBOSE(Format, ...) UE_LOG(Log{{cookiecutter.plugin_namespace}}Shader, Verbose, Format, ##__VA_ARGS__)
#define GK{{cookiecutter.plugin_namespace}}_VERYVERBOSE(Format, ...) UE_LOG(Log{{cookiecutter.plugin_namespace}}Shader, VeryVerbose, Format, ##__VA_ARGS__)

DECLARE_STATS_GROUP(TEXT("{{cookiecutter.plugin_name}}"), STATGROUP_{{cookiecutter.plugin_namespace}}Shader, STATCAT_Advanced);
