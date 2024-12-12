import * as PIXI from 'pixi.js';

export function loadAssets(sprites, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add sprites using their keys
  Object.entries(sprites).forEach(([key, sprite]) => {
    loader.add(key, sprite.path);
  });

  loader.load(() => {
    onComplete();
  });
}
