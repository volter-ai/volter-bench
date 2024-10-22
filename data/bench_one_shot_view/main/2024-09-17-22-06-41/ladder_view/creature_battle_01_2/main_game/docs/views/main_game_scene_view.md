# MainGameSceneView

This is a document describing the main game scene of the pokemon-like creature battler game. 

The screen is divided into two major areas; a battlefield, and buttons to interact that appear below.

## Battlefield Display

The battlefield shows:
- player creature - the player's creature, and their status
- opponent creature - the opponent's creature, and their status

## User Interface

There should be a HUD displaying a game-like interface which shows stats, etc.

The HUD should appear as a nav bar at the top of the screen.

## Choices

The view during combat should show each available skill `Thing` as a button, even though they are not buttons.  These should use the thing interaction API with the ID of the `Thing` rather than a typical button slug.