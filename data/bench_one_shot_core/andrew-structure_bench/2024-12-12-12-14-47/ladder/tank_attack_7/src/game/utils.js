import * as PIXI from 'pixi.js';

export const loadAssets = (sprites, onComplete) => {
  const loader = PIXI.Loader.shared;
  
  // Add all sprite paths to the loader
  Object.values(sprites).forEach(sprite => {
    loader.add(sprite.path, sprite.path);
  });

  // Start loading and call onComplete when done
  loader.load(() => {
    onComplete();
  });
};
