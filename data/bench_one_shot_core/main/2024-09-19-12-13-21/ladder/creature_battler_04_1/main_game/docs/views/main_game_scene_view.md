# MainGameSceneView

This is a document describing the main game scene of the pokemon-like creature battler game. 

The screen is divided into two major areas; a battlefield display area that occupies the upper 2/3 of the screen and a user interface area that occupies the lower 1/3 of the screen.

## Battlefield Display

The upper 2/3 of the screen are devoted to displaying the combatants, their status, and their attack animations. This display is divided into roughly four subareas. Going counterclockwise from the bottom left:
- Bottom-left, player creature - The bottom-left corner displays the player's active creature. This should use the creature's back image, with a shadow or platform drawn underneath it representing the physical space that it occupies. This could have hints of grass, waves, sand, or whatever environmental elements from where the battle is taking place.
- Bottom-right, player creature status - The bottom-right corner displays the player's active creature's status. This includes the creature's name and health. HP should be displayed as a bar, with the relative size representing hp as a fraction of max hp.
- Top-right, opponent creature - The top-right corner displays the opponent's active creature. This should use the creature's front image, with a shadow or platform drawn underneath it representing the physical space that it occupies. This could have hints of grass, waves, sand, or whatever environmental elements from where the battle is taking place.
- Top-left, opponent creature status - The top-left corner displays the opponent's active creature's status. This includes the creature's name and health. HP should be displayed as a bar, with the relative size representing hp as a fraction of max hp.

## User Interface

The lower 1/3 of the screen displays the user interface. This section provides the buttons and choices that the player can interact. Whenever the game is displaying messages, they occupy this space in the place of buttons until they are done being displayed. Whenever choices are displayed in this area, they are arranged in a 2x2 grid.