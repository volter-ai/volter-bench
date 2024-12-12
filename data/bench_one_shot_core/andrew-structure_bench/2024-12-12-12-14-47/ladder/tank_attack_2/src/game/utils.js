import * as PIXI from 'pixi.js';

export function loadAssets(assetManifest, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add all sprites to the loader
  Object.entries(assetManifest).forEach(([key, sprite]) => {
    loader.add(key, sprite.path);
  });

  // Start loading and call onComplete when done
  loader.load(() => {
    onComplete();
  });
}
