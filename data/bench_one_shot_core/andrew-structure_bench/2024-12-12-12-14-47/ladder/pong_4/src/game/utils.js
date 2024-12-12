// src/render/utils.js

import * as PIXI from 'pixi.js';

export class ObjectPool {
  constructor(createFn, resetFn = (obj) => obj) {
    this.createFn = createFn;
    this.resetFn = resetFn;
    this.pool = [];
  }

  get() {
    if (this.pool.length === 0) {
      return this.createFn();
    }
    return this.pool.pop();
  }

  release(object) {
    this.resetFn(object);
    this.pool.push(object);
  }
}


export function loadAssets(ASSET_MANIFEST, callback) {
    const loader = new PIXI.Loader();
    loader.baseUrl = window.location.pathname;

    Object.keys(ASSET_MANIFEST).forEach(assetName => {
      const path = ASSET_MANIFEST[assetName].path;
      loader.add(assetName, path);        // Add with manifest name
      loader.add(path, path);             // Add with unedited path
    });

    // Add default texture
    loader.add('default', 'assets/default.png');
    loader.add('assets/default.png', 'assets/default.png');

    loader.load((loader, resources) => {
      // Check if any textures failed to load and replace with default
      Object.keys(resources).forEach(key => {
        if (key !== 'default' && resources[key].error) {
          console.warn(`Failed to load texture: ${key}. Using default texture.`);
          PIXI.Texture.removeFromCache(key);
          PIXI.Texture.addToCache(resources.default.texture, key);
          PIXI.Texture.addToCache(resources.default.texture, ASSET_MANIFEST[key].path);
        }
      });
      if (callback) callback();
    });
}