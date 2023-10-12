// {{cookiecutter.copyright}}

#pragma once

// Unreal Engine
#include "CoreMinimal.h"
#include "Engine/EngineTypes.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "Kismet/KismetMathLibrary.h"
#include "GenericTeamAgentInterface.h"

// Generated
#include "{{cookiecutter.plugin_namespace}}Library.generated.h"


/**
 * Helper functions
 */
UCLASS()
class {{cookiecutter.plugin_upper}}_API U{{cookiecutter.plugin_name}}Library: public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

    public:
    UFUNCTION(BlueprintPure, BlueprintCallable, Category = "Version")
    static void GetVersionInfo(FString& GitCommitHash, FString& GitTag, FString& Date);
};
