// {{cookiecutter.copyright}}

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"


class F{{cookiecutter.plugin_name}}Module : public IModuleInterface
{
public:

	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
