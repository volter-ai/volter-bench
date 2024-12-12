import * as PIXI from 'pixi.js';

export function loadAssets(assetManifest, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add all assets to the loader
  Object.keys(assetManifest).forEach(key => {
    loader.add(key, assetManifest[key].path);
  });

  // Start loading
  loader.load((loader, resources) => {
    onComplete();
  });
}
