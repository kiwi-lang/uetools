// {{cookiecutter.copyright}}

#pragma once


// Gamekit
#include "{{cookiecutter.plugin_name}}.h"

// Unreal Engine
#include "GameFramework/GameModeBase.h"

// Generated
#include "{{cookiecutter.plugin_namespace}}GameMode.generated.h"


UCLASS(minimalapi)
class A{{cookiecutter.plugin_namespace}}GameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	A{{cookiecutter.plugin_namespace}}GameMode();
};

