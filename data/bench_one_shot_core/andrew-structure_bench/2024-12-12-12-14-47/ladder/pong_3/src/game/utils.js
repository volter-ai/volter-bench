export const loadAssets = (sprites, onComplete) => {
  const loader = PIXI.Loader.shared;
  
  // Add all sprites to the loader
  Object.keys(sprites).forEach(key => {
    loader.add(key, sprites[key].path);
  });

  // Start loading and call onComplete when done
  loader.load(() => {
    onComplete();
  });
};
