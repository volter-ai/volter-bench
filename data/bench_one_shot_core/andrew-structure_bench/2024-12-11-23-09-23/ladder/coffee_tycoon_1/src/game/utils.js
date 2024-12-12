import * as PIXI from 'pixi.js';

export function loadAssets(sprites, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add all sprites to loader
  Object.entries(sprites).forEach(([key, sprite]) => {
    loader.add(key, sprite.path);
  });

  // Start loading
  loader.load(() => {
    onComplete();
  });
}
