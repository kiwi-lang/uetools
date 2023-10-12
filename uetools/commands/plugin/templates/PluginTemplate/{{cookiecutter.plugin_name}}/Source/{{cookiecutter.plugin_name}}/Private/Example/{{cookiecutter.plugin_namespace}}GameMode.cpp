// {{cookiecutter.copyright}}

// Include
#include "{{cookiecutter.plugin_namespace}}GameMode.h"

// Gamekit
#include "{{cookiecutter.plugin_namespace}}PlayerController.h"
#include "{{cookiecutter.plugin_namespace}}Chracter.h"

// Unreal Engine
#include "UObject/ConstructorHelpers.h"


A{{cookiecutter.plugin_namespace}}GameMode::A{{cookiecutter.plugin_namespace}}GameMode()
{
	// use our custom PlayerController class
	PlayerControllerClass = A{{cookiecutter.plugin_namespace}}PlayerController::StaticClass();
    DefaultPawnClass      = A{{cookiecutter.plugin_namespace}}Character::StaticClass();

    // Pawn             :
    // HUD Class        :
    // Player Controller:
    // GameState        :
    // PlayerState      :
    // Spectator Class  :
}
