import React from 'react';
import ReactDOM from 'react-dom/client';
import WebFontProvider from './WebFontProvider'
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <WebFontProvider>
    <App />
  </WebFontProvider>
);
