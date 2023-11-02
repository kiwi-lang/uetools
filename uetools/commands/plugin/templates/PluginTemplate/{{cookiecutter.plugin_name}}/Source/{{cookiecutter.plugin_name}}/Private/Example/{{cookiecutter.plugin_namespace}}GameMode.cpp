// {{cookiecutter.copyright}}

// Include
#include "{{cookiecutter.plugin_namespace}}GameMode.h"

// Gamekit
#include "{{cookiecutter.plugin_namespace}}PlayerController.h"
#include "{{cookiecutter.plugin_namespace}}Character.h"
#include "{{cookiecutter.plugin_namespace}}GameState.h"

// Unreal Engine
#include "UObject/ConstructorHelpers.h"


A{{cookiecutter.plugin_namespace}}GameMode::A{{cookiecutter.plugin_namespace}}GameMode()
{
	// use our custom PlayerController class
	PlayerControllerClass = A{{cookiecutter.plugin_namespace}}PlayerController::StaticClass();
    DefaultPawnClass      = A{{cookiecutter.plugin_namespace}}Character::StaticClass();
    GameStateClass        = A{{cookiecutter.plugin_namespace}}GameState::StaticClass();

    // DefaultPawnClass    = A{{cookiecutter.plugin_namespace}}Pawn::StaticClass();
    // HUDClass            = A{{cookiecutter.plugin_namespace}}HUD::StaticClass();
    // PlayerStateClass    = A{{cookiecutter.plugin_namespace}}PlayerState::StaticClass();
    // SpectatorClass      = A{{cookiecutter.plugin_namespace}}SpecatorPawn::StaticClass();
}
