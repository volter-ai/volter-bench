import * as PIXI from 'pixi.js';

export function loadAssets(spriteManifest, onComplete) {
  const loader = new PIXI.Loader();
  
  // Add all sprites to the loader
  Object.entries(spriteManifest).forEach(([key, sprite]) => {
    loader.add(key, sprite.path);
  });

  loader.load((loader, resources) => {
    // Create and cache textures
    Object.keys(resources).forEach(key => {
      if (resources[key].texture) {
        PIXI.Texture.addToCache(resources[key].texture, spriteManifest[key].path);
      }
    });

    if (onComplete) {
      onComplete();
    }
  });

  loader.onError.add((error) => {
    console.error("Error loading assets:", error);
  });
}
