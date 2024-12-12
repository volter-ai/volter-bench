import * as PIXI from 'pixi.js';

export const loadAssets = (sprites, onComplete) => {
  const loader = PIXI.Loader.shared;
  
  // Add each sprite to the loader using the key
  Object.entries(sprites).forEach(([key, sprite]) => {
    loader.add(key, sprite.path);
  });

  loader.load((loader, resources) => {
    onComplete();
  });
};
