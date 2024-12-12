// src/ui/DebugUI.js

import React, { useState, useEffect } from 'react';

const DebugUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;

  return (
    <div style={{ position: 'absolute', top: '10px', right: '10px', backgroundColor: 'white', padding: '10px' }}>
      <h3>Debug Controls</h3>
      {/* Add debug controls and displays as needed */}
    </div>
  );
};

export default DebugUI;