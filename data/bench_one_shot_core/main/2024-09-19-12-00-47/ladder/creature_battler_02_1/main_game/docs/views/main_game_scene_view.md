# MainGameSceneView

This is a document describing the main game scene of the pokemon-like creature battler game. 

The screen is divided into two major areas; a battlefield, and buttons to interact that appear below.

## Battlefield Display

The battlefield shows:
- player creature - the player's creature, and their status
- opponent creature - the opponent's creature, and their status

## User Interface

The UI component shows:
- available buttons

But also, it should show each available skill `Thing` as a button, even though they are not buttons.  These should use the thing interaction API with the ID of the `Thing` rather than a typical button slug.