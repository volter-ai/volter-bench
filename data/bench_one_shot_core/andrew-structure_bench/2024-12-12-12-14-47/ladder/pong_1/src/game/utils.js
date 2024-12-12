import * as PIXI from 'pixi.js';

export function loadAssets(assetManifest, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add all assets to the loader
  Object.entries(assetManifest).forEach(([key, asset]) => {
    loader.add(key, asset.path);
  });

  // Start loading and call onComplete when done
  loader.load(() => {
    onComplete();
  });
}
