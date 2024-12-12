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
    {children} ({cost} points)
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#d3d3d3' }}>
    <p>Score: {game.score}</p>
    <p>Paddle Size: {game.paddleSize} | Ball Speed: {game.ballSpeed} | Points/Hit: {game.pointsPerHit}</p>
    <p>Paddle Speed: {game.paddleSpeed} | Accuracy: {(game.paddleAccuracy * 100).toFixed(1)}%</p>
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
        <Button onClick={() => game.upgradePaddleSize()} cost={game.paddleSizeCost}>
          Upgrade Paddle Size
        </Button>
        <Button onClick={() => game.upgradeBallSpeed()} cost={game.ballSpeedCost}>
          Upgrade Ball Speed
        </Button>
        <Button onClick={() => game.upgradePointsPerHit()} cost={game.pointsPerHitCost}>
          Upgrade Points Per Hit
        </Button>
        <Button onClick={() => game.upgradePaddleSpeed()} cost={game.paddleSpeedCost}>
          Upgrade Paddle Speed
        </Button>
        <Button onClick={() => game.upgradePaddleAccuracy()} cost={game.paddleAccuracyCost}>
          Upgrade Paddle Accuracy
        </Button>
      </div>
    </div>
  );
};

export default GameUI;
