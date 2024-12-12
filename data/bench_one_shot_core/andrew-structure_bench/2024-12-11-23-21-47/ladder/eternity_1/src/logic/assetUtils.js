// Import default sprites that are already in the correct format
import { SPRITES as DEFAULT_SPRITES } from './assetManifest.js';

// Initialize SPRITES object
let SPRITES = null;
let DEBUG_MODE = false;

// Initialize the module
function initialize() {
  if (!SPRITES) {
    // Non-browser environment - use defaults directly
    if (typeof window === 'undefined' || DEBUG_MODE) {
      SPRITES = DEFAULT_SPRITES;
      return Promise.resolve();
    }

    // Browser environment - try to fetch manifest
    return fetch('/assets/manifest.json')
      .then(response => response.json())
      .then(manifest => createSpritesFromManifest(manifest))
      .catch(error => {
        console.warn('⚠️ Unable to load asset manifest, falling back to default sprites:', error);
        return DEFAULT_SPRITES;
      })
      .then(sprites => {
        SPRITES = sprites;
      });
  }
  return Promise.resolve();
}

// Convert manifest data to SPRITES format
function createSpritesFromManifest(manifest) {
  const gameAssets = manifest.bundles.find(bundle => bundle.name === 'gameAssets');
  if (!gameAssets) {
    throw new Error('Game assets bundle not found in manifest');
  }

  return gameAssets.assets.reduce((sprites, asset) => {
    sprites[asset.alias] = {
      srcs: asset.src,
      width: asset.data.width,
      height: asset.data.height,
      ...(asset.data.variations && { variations: asset.data.variations })
    };
    return sprites;
  }, {});
}

// Get sprite URL with optional variation
function getSpriteUrl(spriteId, variation = null) {
  if (!SPRITES) {
    throw new Error('Asset utils not initialized. Call initialize() first');
  }

  const sprite = SPRITES[spriteId];
  if (!sprite) {
    throw new Error(`Sprite ${spriteId} not found`);
  }

  // Check if the sprite URL contains a variation placeholder
  const requiresVariation = sprite.srcs.includes('{variation}');

  if (requiresVariation && !variation) {
    throw new Error(`Sprite ${spriteId} requires a variation but none was provided. Valid variations are: ${sprite.variations.join(', ')}`);
  }

  if (variation) {
    // Check if sprite supports variations
    if (!sprite.variations) {
      throw new Error(`Sprite ${spriteId} does not support variations`);
    }

    // Validate the variation exists
    if (!sprite.variations.includes(variation)) {
      throw new Error(`Invalid variation ${variation} for sprite ${spriteId}. Valid variations are: ${sprite.variations.join(', ')}`);
    }

    // Replace the {variation} placeholder in the URL
    return sprite.srcs.replace('{variation}', variation);
  }

  // Return the direct URL if no variation is needed
  return sprite.srcs;
}

export { initialize, getSpriteUrl };