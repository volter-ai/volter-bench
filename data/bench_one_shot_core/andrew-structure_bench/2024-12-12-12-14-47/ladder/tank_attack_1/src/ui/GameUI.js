import React, { useState, useEffect } from 'react';

const Button = ({ onClick, children, cost, disabled }) => (
  <button 
    onClick={onClick} 
    disabled={disabled}
    style={{
      margin: '5px',
      padding: '5px 10px',
      fontSize: '14px',
      color: '#d3d3d3',
      border: 'none',
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: disabled ? '#4a2b7c' : '#7C45CB',
      opacity: disabled ? 0.7 : 1,
    }}
  >
    {children} ({cost} coins)
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#d3d3d3' }}>
    <p>Coins: {Math.floor(game.coins)} | Tanks: {game.tanks.children.length}/{game.maxTanks} | Damage: {game.tankDamage.toFixed(1)} | Fire Rate: {game.tankFireRate.toFixed(1)} | Multi-shot: {game.multiShot}</p>
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
        <Button onClick={() => game.upgradeTankDamage()} cost={game.upgradeCosts.TANK_DAMAGE} disabled={!game.canAffordUpgrade(game.upgradeCosts.TANK_DAMAGE)}>Upgrade Damage</Button>
        <Button onClick={() => game.upgradeTankSpeed()} cost={game.upgradeCosts.TANK_SPEED} disabled={!game.canAffordUpgrade(game.upgradeCosts.TANK_SPEED)}>Upgrade Speed</Button>
        <Button onClick={() => game.upgradeTankFireRate()} cost={game.upgradeCosts.TANK_FIRE_RATE} disabled={!game.canAffordUpgrade(game.upgradeCosts.TANK_FIRE_RATE)}>Upgrade Fire Rate</Button>
        <Button onClick={() => game.upgradeMaxTanks()} cost={game.upgradeCosts.MAX_TANKS} disabled={!game.canAffordUpgrade(game.upgradeCosts.MAX_TANKS)}>Increase Max Tanks</Button>
        <Button onClick={() => game.upgradeMultiShot()} cost={game.upgradeCosts.MULTI_SHOT} disabled={!game.canAffordUpgrade(game.upgradeCosts.MULTI_SHOT)}>Upgrade Multi-shot</Button>
        <Button onClick={() => game.upgradeBaseCoinValue()} cost={game.upgradeCosts.BASE_COIN_VALUE} disabled={!game.canAffordUpgrade(game.upgradeCosts.BASE_COIN_VALUE)}>Upgrade Coin Value</Button>
      </div>
    </div>
  );
};

export default GameUI;
