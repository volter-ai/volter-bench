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
    <p>Coins: {Math.floor(game.currency)} | Runners: {game.runnerCount} | Tracks: {game.trackCount} | Speed: {game.runnerSpeed.toFixed(1)} | Coin Value: {game.coinValue.toFixed(1)} | Spawn Rate: {game.coinSpawnRate.toFixed(1)}/s</p>
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
        <Button onClick={() => game.upgradeRunnerSpeed()} cost={game.costs.RUNNER_SPEED}>Upgrade Runner Speed</Button>
        <Button onClick={() => game.upgradeRunnerCount()} cost={game.costs.RUNNER_COUNT}>Add Runner</Button>
        <Button onClick={() => game.upgradeTrackCount()} cost={game.costs.TRACK_COUNT}>Add Track</Button>
        <Button onClick={() => game.upgradeCoinValue()} cost={game.costs.COIN_VALUE}>Increase Coin Value</Button>
        <Button onClick={() => game.upgradeCoinSpawnRate()} cost={game.costs.COIN_SPAWN_RATE}>Increase Coin Spawn Rate</Button>
        <Button onClick={() => game.upgradeCollisionRadius()} cost={game.costs.COLLISION_RADIUS}>Increase Collection Range</Button>
      </div>
    </div>
  );
};

export default GameUI;
