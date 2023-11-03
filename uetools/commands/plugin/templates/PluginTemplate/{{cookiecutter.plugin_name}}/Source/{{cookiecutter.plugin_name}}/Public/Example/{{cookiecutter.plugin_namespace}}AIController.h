// {{cookiecutter.copyright}}

#pragma once


// Gamekit

// Unreal Engine
#include "AIController.h"

// Generated
#include "{{cookiecutter.plugin_namespace}}AIController.generated.h"


UCLASS()
class {{cookiecutter.plugin_upper}}_API A{{cookiecutter.plugin_namespace}}AIController : public AAIController 
{
	GENERATED_BODY()

public:
	virtual void BeginPlay();
};


