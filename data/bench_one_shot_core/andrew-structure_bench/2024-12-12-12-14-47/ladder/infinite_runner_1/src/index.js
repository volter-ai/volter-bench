import React from 'react';
import ReactDOM from 'react-dom/client';
import Game from './Game';
import WebFontProvider from './WebFontProvider';

// Get URL search params
const params = new URLSearchParams(window.location.search);
const isDebug = params.get('debug') === 'true';

// Dynamic import for gameAI if debug=true
if (isDebug) {
  import('./GameAI').then(module => {
    // gameAI is available as module.default
    window.gameAI = module.default;
  });
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <WebFontProvider>
    <Game />
  </WebFontProvider>
);