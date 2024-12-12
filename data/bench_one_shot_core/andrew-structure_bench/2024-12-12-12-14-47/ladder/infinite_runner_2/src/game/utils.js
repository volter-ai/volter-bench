export const loadAssets = (sprites, onComplete) => {
  const loader = new PIXI.Loader();
  
  Object.values(sprites).forEach(sprite => {
    loader.add(sprite.path, sprite.path);
  });

  loader.load(() => {
    onComplete();
  });
};
