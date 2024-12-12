import React, { useState, useEffect } from 'react';

const Button = ({ onClick, children, cost }) => (
  <button onClick={onClick} style={{
    margin: '5px',
    padding: '5px 10px',
    fontSize: '14px',
    color: '#FFFFFF',
    border: 'none',
    cursor: 'pointer',
    backgroundColor: '#4A90E2',
  }}>
    {children} (${cost})
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#FFFFFF' }}>
    <p>Money: ${game.money} | Baristas: {game.baristaCount} | Customers: {game.customers?.children?.length || 0}/{game.customerCapacity} | Coffee Price: ${game.coffeePrice}</p>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current || !gameRef.current.ready) return null;

  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%', color: '#FFFFFF' }}>
      <HUD game={game} />
      <div style={{ position: 'absolute', bottom: '10px', left: '10px', right: '10px', textAlign: 'center' }}>
        <Button onClick={() => game.upgradeBarista()} cost={game.baristaCost}>
          Hire Barista
        </Button>
        <Button onClick={() => game.upgradeBaristaSpeed()} cost={game.baristaSpeedCost}>
          Upgrade Barista Speed
        </Button>
        <Button onClick={() => game.upgradeCustomerCapacity()} cost={game.customerCapacityCost}>
          Increase Customer Capacity
        </Button>
        <Button onClick={() => game.upgradeCoffeePrice()} cost={game.coffeePriceCost}>
          Increase Coffee Price
        </Button>
        <Button onClick={() => game.upgradeProcessingSpeed()} cost={game.processingSpeedCost}>
          Upgrade Processing Speed
        </Button>
      </div>
    </div>
  );
};

export default GameUI;
