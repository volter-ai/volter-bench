import * as PIXI from 'pixi.js';

export function loadAssets(assetManifest, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add all assets to the loader using the key, not the path
  Object.entries(assetManifest).forEach(([key, config]) => {
    loader.add(key, config.path);
  });

  // Start loading
  loader.load(() => {
    onComplete();
  });
}
