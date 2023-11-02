// {{cookiecutter.copyright}}

#pragma once

// Gamekit

// Unreal Engine
#include "GameFramework/GameStateBase.h"

// Generated
#include "{{cookiecutter.plugin_namespace}}GameState.generated.h"


UCLASS(minimalapi)
class A{{cookiecutter.plugin_namespace}}GameState : public AGameStateBase 
{

    GENERATED_BODY()

public:
    A{{cookiecutter.plugin_namespace}}GameState();
};
