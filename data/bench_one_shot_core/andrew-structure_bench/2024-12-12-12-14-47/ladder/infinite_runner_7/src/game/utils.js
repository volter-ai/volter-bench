import * as PIXI from 'pixi.js';

export function loadAssets(assetManifest, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add all sprites to loader
  Object.entries(assetManifest).forEach(([key, sprite]) => {
    loader.add(key, sprite.path);
  });

  // Start loading
  loader.load((loader, resources) => {
    onComplete();
  });
}
