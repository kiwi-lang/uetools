// {{cookiecutter.copyright}}

#pragma once


// Gamekit
#include "{{cookiecutter.plugin_name}}.h"

// Unreal Engine
#include "GameFramework/Character.h"

// Generated
#include "{{cookiecutter.plugin_namespace}}Character.generated.h"




UCLASS(Blueprintable)
class A{{cookiecutter.plugin_namespace}}Character : public ACharacter
{
	GENERATED_BODY()

public:
	A{{cookiecutter.plugin_namespace}}Character();

	// Called every frame.
	virtual void Tick(float DeltaSeconds) override;
};
