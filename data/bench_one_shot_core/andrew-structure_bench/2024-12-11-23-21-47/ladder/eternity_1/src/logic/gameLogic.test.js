import GameLogic from './gameLogic';
import { STORY_CONTENT } from './storyContent';
import { CHARACTERS, LOCATIONS } from './gameData';
import { initialize } from './assetUtils';

describe('GameLogic', () => {
  let game;

  beforeAll(() => {
    game = new GameLogic();
    return initialize();
  });

  describe('validate story content', () => {
    test('validate all story content', () => {
      const errors = [];
      const game = new GameLogic();

      // Validate all story content
      Object.entries(STORY_CONTENT.chapters).forEach(([chapterId, chapter]) => {
        // Skip validation for placeholder content
        if (chapter.isPlaceholder) return;

        Object.entries(chapter.scenes).forEach(([sceneId, scene]) => {
          // Validate location
          try {
            game.getSpriteUrl(scene.location);
          } catch (error) {
            errors.push(`Invalid location ${scene.location} in chapter ${chapterId}, scene ${sceneId}`);
          }

          Object.entries(scene.beats).forEach(([beatId, beat]) => {
            beat.lines.forEach((line, lineIndex) => {
              // Validate character sprites
              if (line.type === 'dialog') {
                if (!CHARACTERS[line.speaker]) {
                  errors.push(`Invalid character ${line.speaker} in chapter ${chapterId}, scene ${sceneId}, beat ${beatId}, line ${lineIndex}`);
                }
                if (!line.noSpeakerSprite) {
                  try {
                    game.getSpriteUrl(line.speaker, line.variation);
                  } catch (error) {
                    errors.push(`${error.message} in chapter ${chapterId}, scene ${sceneId}, beat ${beatId}, line ${lineIndex}`);
                  }
                }
              }

              // Validate choices
              if (line.type === 'choice') {
                line.options.forEach((option, optionIndex) => {
                  if (!option.next && !option.next.isGameOver) {
                    errors.push(`Missing next for choice option ${optionIndex} in chapter ${chapterId}, scene ${sceneId}, beat ${beatId}, line ${lineIndex}`);
                  }
                });
              }
            });

            // Validate next references
            if (beat.next && !beat.next.isGameOver) {
              const { chapter, scene, beat: nextBeat } = beat.next;
              if (!STORY_CONTENT.chapters[chapter]?.scenes[scene]?.beats[nextBeat]) {
                errors.push(`Invalid next reference "${chapter}.${scene}.${nextBeat}" in chapter ${chapterId}, scene ${sceneId}, beat ${beatId}`);
              }
            }
          });
        });
      });

      if (errors.length > 0) {
        throw new Error('Story validation failed:\n' + errors.join('\n'));
      }
    });
  });

  describe('full simulation', () => {
    test('simulate the game many times until the end', () => {
      // Skip simulation if all content is placeholder
      if (Object.values(STORY_CONTENT.chapters).every(chapter => chapter.isPlaceholder)) {
        return;
      }

      const endingsSeen = new Set();
      
      // Run 100 simulations
      for (let i = 0; i < 100; i++) {
        game.reset();
        let isGameOver = false;

        // Run 1000 steps in the story
        for (let j = 0; j < 1000; j++) {
          const { content, location } = game.getCurrentContent();
          
          // Validate location sprite
          game.getSpriteUrl(location);
          
          // Validate character sprites if dialog
          if (content.type === 'dialog' && !content.noSpeakerSprite) {
            game.getSpriteUrl(content.speaker, content.variation);
          }

          if (content.type === 'choice') {
            // Make random choice
            const choiceIndex = Math.floor(Math.random() * content.options.length);
            const result = game.makeChoice(choiceIndex);
            isGameOver = result.isGameOver;
          } else {
            const result = game.advance();
            isGameOver = result.isGameOver;
          }

          if (isGameOver) {
            break;
          }
        }

        if (!isGameOver) {
          throw new Error('1000 steps in the simulation were run but we did not reach game over');
        }

        // Record which ending was reached
        const { beat } = game.position;
        endingsSeen.add(beat);
      }
    });
  });
});
