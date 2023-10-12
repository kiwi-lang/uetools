// {{cookiecutter.copyright}}

#pragma once

// Gamekit
#include "{{cookiecutter.plugin_name}}.h"

// Unreal Engine
#include "GameFramework/PlayerController.h"

// Generated
#include "{{cookiecutter.plugin_namespace}}PlayerController.generated.h"


UCLASS()
class {{cookiecutter.plugin_upper}}_API A{{cookiecutter.plugin_namespace}}PlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	virtual void BeginPlay();
};


