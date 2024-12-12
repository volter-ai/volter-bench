import React, { useState, useEffect } from 'react';

const Button = ({ onClick, children, cost }) => (
  <button onClick={onClick} style={{
    margin: '5px',
    padding: '5px 10px',
    fontSize: '14px',
    color: '#d3d3d3',
    border: 'none',
    cursor: 'pointer',
    backgroundColor: '#7C45CB',
  }}>
    {children} ({cost} coins)
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#d3d3d3' }}>
    <p>Coins: {Math.floor(game.score)} | Runners: {game.runnerCount} | Tracks: {game.trackCount} | Runner Speed: {game.runnerSpeed.toFixed(1)} | Coin Value: {game.coinValue.toFixed(1)} | Spawn Rate: {game.coinSpawnRate.toFixed(1)}</p>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%', color: '#d3d3d3' }}>
      <HUD game={game} />
      <div style={{ position: 'absolute', bottom: '10px', left: '10px', right: '10px', textAlign: 'center' }}>
        <Button onClick={() => game.upgradeRunnerSpeed()} cost={game.runnerSpeedCost}>Upgrade Runner Speed</Button>
        <Button onClick={() => game.upgradeCoinSpawnRate()} cost={game.coinSpawnRateCost}>Upgrade Spawn Rate</Button>
        <Button onClick={() => game.upgradeCoinValue()} cost={game.coinValueCost}>Upgrade Coin Value</Button>
        <Button onClick={() => game.upgradeRunnerCount()} cost={game.runnerCountCost}>Add Runner</Button>
        <Button onClick={() => game.upgradeTrackCount()} cost={game.trackCountCost}>Add Track</Button>
      </div>
    </div>
  );
};

export default GameUI;
