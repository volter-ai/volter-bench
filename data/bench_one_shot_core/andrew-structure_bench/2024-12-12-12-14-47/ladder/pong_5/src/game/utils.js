import * as PIXI from 'pixi.js';

export function loadAssets(assetManifest, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add each sprite to the loader
  Object.entries(assetManifest).forEach(([key, sprite]) => {
    loader.add(key, sprite.path);
  });

  loader.load((loader, resources) => {
    onComplete();
  });
}
