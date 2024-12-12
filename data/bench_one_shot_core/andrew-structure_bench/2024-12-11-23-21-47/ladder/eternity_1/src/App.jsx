import React, { useEffect, useState } from 'react';
import GameLogic from './logic/gameLogic';
import Home from './pages/Home';
import Story from './pages/Story';
import Loading from './pages/Loading';
import { initialize } from './logic/assetUtils';

window.gameLogic = new GameLogic();

export default function App() {
  const [currentPage, setCurrentPage] = useState('loading');
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadAssets = async () => {
      try {
        await initialize();
        setCurrentPage('home');
      } catch (err) {
        setError(err.message);
        console.error('Failed to load game assets:', err);
      }
    };

    loadAssets();
  }, []);

  const handleStartGame = () => {
    window.gameLogic.reset();
    setCurrentPage('story');
  };

  const handleLeaveStory = () => {
    setCurrentPage('home');
  };

  if (currentPage === 'loading') {
    return <Loading error={error} />;
  }

  return (
    <>
      {currentPage === 'home' && (
        <Home onStartGame={handleStartGame} />
      )}
      {currentPage === 'story' && (
        <Story
          gameLogic={window.gameLogic}
          onLeaveStory={handleLeaveStory}
        />
      )}
    </>
  );
}