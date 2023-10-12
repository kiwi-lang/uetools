// {{cookiecutter.copyright}}

#pragma once

#include "Modules/ModuleManager.h"

class F{{cookiecutter.plugin_name}}ShaderModule: public IModuleInterface
{
    public:
    /** IModuleInterface implementation */
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;
};
