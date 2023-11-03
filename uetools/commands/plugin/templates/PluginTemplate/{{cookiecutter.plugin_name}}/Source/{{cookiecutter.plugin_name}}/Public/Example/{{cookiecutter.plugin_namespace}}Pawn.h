// {{cookiecutter.copyright}}

#pragma once


// Gamekit

// Unreal Engine
#include "GameFramework/Pawn.h"

// Generated
#include "{{cookiecutter.plugin_namespace}}Pawn.generated.h"



UCLASS()
class {{cookiecutter.plugin_upper}}_API A{{cookiecutter.plugin_namespace}}Pawn : public APawn 
{
	GENERATED_BODY()

public:
	virtual void BeginPlay();
};


