import * as PIXI from 'pixi.js';

export const loadAssets = (sprites, onComplete) => {
    // Convert sprite paths to array for loader
    const resources = Object.values(sprites).map(sprite => sprite.path);
    
    // Add to loader
    resources.forEach(resource => {
        PIXI.Loader.shared.add(resource);
    });

    // Start loading and call onComplete when done
    PIXI.Loader.shared.load(() => {
        onComplete();
    });
};
