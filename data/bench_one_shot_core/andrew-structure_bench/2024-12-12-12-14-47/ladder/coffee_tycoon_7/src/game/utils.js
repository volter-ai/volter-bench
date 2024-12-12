import * as PIXI from 'pixi.js';

export function loadAssets(ASSET_MANIFEST, onComplete) {
    const loader = PIXI.Loader.shared;
    
    // Add all sprites to loader
    Object.keys(ASSET_MANIFEST).forEach(key => {
        loader.add(key, ASSET_MANIFEST[key].path);
    });

    // Start loading
    loader.load((loader, resources) => {
        onComplete();
    });
}
