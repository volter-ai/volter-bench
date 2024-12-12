import { CHARACTERS, LOCATIONS } from './gameData';
import { v4 } from 'uuid';
import { STORY_CONTENT } from './storyContent';
import { getSpriteUrl } from './assetUtils'

const deepClone = (obj) => JSON.parse(JSON.stringify(obj));

export default class GameLogic {
  constructor() {
    this.position = this.getInitialPosition();
  }

  getInitialPosition() {
    const firstChapter = Object.keys(STORY_CONTENT.chapters)[0];
    const firstScene = Object.keys(STORY_CONTENT.chapters[firstChapter].scenes)[0];
    const firstBeat = Object.keys(STORY_CONTENT.chapters[firstChapter].scenes[firstScene].beats)[0];

    return {
      chapter: firstChapter,
      scene: firstScene,
      beat: firstBeat,
      lineIndex: 0
    };
  }

  getSpriteUrl(spriteId, variation = null) {
    return getSpriteUrl(spriteId, variation);
  }

  reset() {
    this.position = this.getInitialPosition();
    return this.position;
  }

  getCurrentContent() {
    const { chapter, scene, beat, lineIndex } = this.position;

    if (!STORY_CONTENT.chapters[chapter]) {
      throw new Error(`Chapter ${chapter} not found`);
    }

    const currentScene = STORY_CONTENT.chapters[chapter].scenes[scene];
    if (!currentScene) {
      throw new Error(`Scene ${scene} not found in chapter ${chapter}`);
    }

    const currentBeat = currentScene.beats[beat];
    if (!currentBeat) {
      throw new Error(`Beat ${beat} not found in scene ${scene}`);
    }

    if (lineIndex >= currentBeat.lines.length) {
      throw new Error(`Line index ${lineIndex} out of bounds`);
    }

    return {
      content: currentBeat.lines[lineIndex],
      location: currentScene.location
    };
  }

  handleTransition(next) {
    if (!next) {
      throw new Error('Cannot advance: no next position specified');
    }

    if (next.isGameOver) {
      return { isGameOver: true };
    }

    if (!next.chapter || !next.scene || !next.beat) {
      throw new Error('Next position must specify chapter, scene and beat');
    }

    this.position = {
      chapter: next.chapter,
      scene: next.scene,
      beat: next.beat,
      lineIndex: 0
    };

    return this.position;
  }

  advance() {
    const { chapter, scene, beat, lineIndex } = this.position;
    const currentScene = STORY_CONTENT.chapters[chapter].scenes[scene];
    const currentBeat = currentScene.beats[beat];

    if (lineIndex + 1 < currentBeat.lines.length) {
      this.position.lineIndex += 1;
      return this.position;
    }

    return this.handleTransition(currentBeat.next);
  }

  makeChoice(choiceIndex) {
    const { content } = this.getCurrentContent();
    if (content.type !== 'choice') {
      throw new Error('Current content is not a choice');
    }

    const choice = content.options[choiceIndex];
    if (!choice) {
      throw new Error(`Invalid choice index: ${choiceIndex}`);
    }

    return this.handleTransition(choice.next);
  }
}
