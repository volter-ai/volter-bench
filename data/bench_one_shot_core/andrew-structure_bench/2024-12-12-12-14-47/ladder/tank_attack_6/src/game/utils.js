import * as PIXI from 'pixi.js';

export const loadAssets = (sprites, onComplete) => {
  // Get all unique sprite paths
  const paths = [...new Set(Object.values(sprites).map(sprite => sprite.path))];
  
  // Create loader
  const loader = PIXI.Loader.shared;
  
  // Add resources
  paths.forEach(path => {
    loader.add(path, path);
  });

  // Load all assets
  loader.load((loader, resources) => {
    onComplete();
  });

  loader.onError.add((error) => {
    console.error("Error loading assets:", error.message || error);
  });
};
