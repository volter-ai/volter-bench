import * as PIXI from 'pixi.js';

export function loadAssets(assetManifest, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add all sprites to loader
  Object.entries(assetManifest).forEach(([key, config]) => {
    loader.add(key, config.path);
  });

  // Start loading and call onComplete when done
  loader.load((loader, resources) => {
    onComplete();
  });
}
