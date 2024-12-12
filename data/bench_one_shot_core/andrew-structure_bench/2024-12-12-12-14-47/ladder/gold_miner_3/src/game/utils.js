import * as PIXI from 'pixi.js';

export function loadAssets(sprites, onComplete) {
    // Create loader
    const loader = PIXI.Loader.shared;
    
    // Add all assets to the loader
    Object.values(sprites).forEach(sprite => {
        loader.add(sprite.path, sprite.path);
    });

    // Load them and call onComplete when done
    loader.load(() => {
        onComplete();
    });
}
