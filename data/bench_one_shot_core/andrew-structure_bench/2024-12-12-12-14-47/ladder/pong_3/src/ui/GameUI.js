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
    position: 'relative',
  }}>
    {children} ({cost} points)
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#d3d3d3' }}>
    <p>Score: {Math.floor(game.score)} | Ball Speed: {game.ballSpeed.toFixed(1)} | Paddle Size: {game.paddleSize.toFixed(1)} | Balls: {game.ballCount} | Paddle Speed: {game.paddleSpeed.toFixed(1)} | Points Multiplier: {game.pointsMultiplier.toFixed(1)}x</p>
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
        <Button onClick={() => game.upgradeBallSpeed()} cost={Math.floor(game.ballSpeedCost)}>Upgrade Ball Speed</Button>
        <Button onClick={() => game.upgradePaddleSize()} cost={Math.floor(game.paddleSizeCost)}>Upgrade Paddle Size</Button>
        <Button onClick={() => game.upgradeBallCount()} cost={Math.floor(game.ballCountCost)}>Add Ball</Button>
        <Button onClick={() => game.upgradePaddleSpeed()} cost={Math.floor(game.paddleSpeedCost)}>Upgrade Paddle Speed</Button>
        <Button onClick={() => game.upgradePointsMultiplier()} cost={Math.floor(game.pointsMultiplierCost)}>Upgrade Points Multiplier</Button>
      </div>
    </div>
  );
};

export default GameUI;
