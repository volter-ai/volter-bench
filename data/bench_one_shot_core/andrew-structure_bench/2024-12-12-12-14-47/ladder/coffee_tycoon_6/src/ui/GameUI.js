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
    {children} (${cost})
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#d3d3d3' }}>
    <p>Money: ${game.money.toFixed(0)} | Baristas: {game.baristaCount} | Coffee Price: ${game.coffeePrice}</p>
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
        <Button onClick={() => game.upgradeBarista()} cost={game.upgradeCosts.barista}>Add Barista</Button>
        <Button onClick={() => game.upgradeBaristaSpeed()} cost={game.upgradeCosts.baristaSpeed}>Upgrade Barista Speed</Button>
        <Button onClick={() => game.upgradeCoffeeEfficiency()} cost={game.upgradeCosts.coffeeEfficiency}>Upgrade Coffee Machine</Button>
        <Button onClick={() => game.upgradeCustomerCapacity()} cost={game.upgradeCosts.customerCapacity}>Increase Customer Capacity</Button>
        <Button onClick={() => game.upgradeCoffeePrice()} cost={game.upgradeCosts.coffeePrice}>Increase Coffee Price</Button>
      </div>
    </div>
  );
};

export default GameUI;
