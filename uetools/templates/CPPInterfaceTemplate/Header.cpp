// Copyright 2023 Mischievous Game, Inc. All Rights Reserved.

#pragma once

// Unreal Engine
#include "CoreMinimal.h"
#include "UObject/Interface.h"

// Generated
#include "GKAbilityPawnInterface.generated.h"


UINTERFACE()
class GKABILITY_API UGKAbilityPawnInterface: public UInterface
{
	GENERATED_UINTERFACE_BODY()
};

/* Basic functions an Actor needs to Implement to support the GKAbility
 * system
 */
class GKABILITY_API IGKAbilityPawnInterface
{
	GENERATED_IINTERFACE_BODY()

    // gkfow::ImplementsInterface(Actor, UGKFogOfWarAgentInterface::StaticClass())
    // Shape = IGKFogOfWarAgentInterface::Execute_GetFogOfWarCollisionShape(Actor);

    // Interfaces from Blueprints
    // TScriptInterface<IGKFogOfWarGameStateInterface> GameState
    // IGenericTeamAgentInterface* GameState.GetInterface()
};
