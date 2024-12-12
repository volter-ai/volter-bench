import * as PIXI from 'pixi.js';

export const loadAssets = (sprites, onComplete) => {
  const loader = PIXI.Loader.shared;
  
  // Add each sprite to the loader
  Object.keys(sprites).forEach(key => {
    loader.add(key, sprites[key].path);
  });

  // Start loading and call onComplete when done
  loader.load((loader, resources) => {
    onComplete();
  });
};
