import * as PIXI from 'pixi.js';

export function loadAssets(assetManifest, onComplete) {
    const loader = new PIXI.Loader();
    
    // Add all assets to the loader
    Object.entries(assetManifest).forEach(([key, config]) => {
        loader.add(key, config.path);
    });

    // Start loading
    loader.load((loader, resources) => {
        // Add textures to cache
        Object.keys(resources).forEach(key => {
            if (resources[key].texture) {
                PIXI.Texture.addToCache(resources[key].texture, assetManifest[key].path);
            }
        });
        
        onComplete();
    });
}
