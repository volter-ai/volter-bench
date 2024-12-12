import * as PIXI from 'pixi.js';

export function loadAssets(assetManifest, onComplete) {
  const loader = PIXI.Loader.shared;
  
  // Add all sprites to the loader
  Object.entries(assetManifest).forEach(([key, sprite]) => {
    loader.add(key, sprite.path);
  });

  // Start loading
  loader.load((loader, resources) => {
    Object.keys(resources).forEach(key => {
      if (resources[key].texture) {
        // Store the loaded texture with the sprite name as the key
        PIXI.Texture.addToCache(resources[key].texture, key);
      }
    });
    
    if (onComplete) {
      onComplete();
    }
  });
}
