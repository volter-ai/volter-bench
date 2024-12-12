import * as PIXI from 'pixi.js';

export function loadAssets(sprites, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add each sprite to the loader
  Object.values(sprites).forEach(sprite => {
    loader.add(sprite.path, sprite.path);
  });

  // Start loading and call onComplete when done
  loader.load(() => {
    onComplete();
  });
}
