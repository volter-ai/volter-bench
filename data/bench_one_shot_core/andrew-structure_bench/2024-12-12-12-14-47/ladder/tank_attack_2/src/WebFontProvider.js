import React, { useEffect } from 'react';
import { FONTS } from './game/fontManifest'; // Adjust the import path as needed

const WebFontProvider = ({ children }) => {
  useEffect(() => {
    // Create a script element to load the WebFontLoader
    const webFontScript = document.createElement('script');
    webFontScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/webfont/1.6.28/webfontloader.js';
    webFontScript.async = true;

    // Configure and load fonts when the script loads
    webFontScript.onload = () => {
      window.WebFont.load({
        google: {
          families: FONTS
        },
        active: () => {
          // Fonts have loaded successfully
          console.log('All fonts have loaded');
          document.documentElement.classList.add('fonts-loaded');
        },
        inactive: () => {
          // Fonts failed to load
          console.warn('Fonts failed to load');
        }
      });
    };

    // Add the script to the document
    document.head.appendChild(webFontScript);

    // Cleanup
    return () => {
      document.head.removeChild(webFontScript);
    };
  }, []);

  return <>{children}</>;
};

export default WebFontProvider;