import React, { useState, useEffect } from 'react';

const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.7)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: 'rgba(20, 20, 35, 0.95)',
        border: '2px solid #7C45CB',
        borderRadius: '8px',
        padding: '20px',
        minWidth: '300px',
        maxWidth: '80%',
        maxHeight: '80%',
        overflow: 'auto',
        boxShadow: '0 0 20px rgba(124, 69, 203, 0.3)',
        color: '#d3d3d3',
        fontFamily: 'Orbitron, sans-serif'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '15px',
          borderBottom: '1px solid #7C45CB',
          paddingBottom: '10px'
        }}>
          <h2 style={{ margin: 0, color: '#fff' }}>{title}</h2>
          <button onClick={onClose} style={{
            background: 'none',
            border: 'none',
            color: '#d3d3d3',
            fontSize: '20px',
            cursor: 'pointer'
          }}>×</button>
        </div>
        {children}
      </div>
    </div>
  );
};

const Button = ({ onClick, children, cost, disabled }) => (
  <button 
    onClick={onClick}
    disabled={disabled}
    style={{
      margin: '5px',
      padding: '8px 15px',
      fontSize: '14px',
      color: disabled ? '#666' : '#fff',
      border: '1px solid #7C45CB',
      borderRadius: '4px',
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: disabled ? '#2a2a2a' : 'rgba(124, 69, 203, 0.2)',
      transition: 'all 0.2s ease',
      fontFamily: 'Orbitron, sans-serif',
      ':hover': {
        backgroundColor: disabled ? '#2a2a2a' : 'rgba(124, 69, 203, 0.4)'
      }
    }}>
    {children} ({cost} coins)
  </button>
);

const MenuButton = ({ onClick, children }) => (
  <button 
    onClick={onClick}
    style={{
      margin: '5px',
      padding: '8px 15px',
      fontSize: '14px',
      color: '#fff',
      border: '1px solid #7C45CB',
      borderRadius: '4px',
      cursor: 'pointer',
      backgroundColor: 'rgba(124, 69, 203, 0.2)',
      transition: 'all 0.2s ease',
      fontFamily: 'Orbitron, sans-serif'
    }}>
    {children}
  </button>
);

const HUD = ({ game }) => (
  <div style={{
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    padding: '15px',
    background: 'linear-gradient(180deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 100%)',
    color: '#fff',
    fontFamily: 'Orbitron, sans-serif'
  }}>
    <div style={{ fontSize: '18px' }}>
      Coins: {Math.floor(game.coinCount)}
    </div>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [showStats, setShowStats] = useState(false);
  const [showUpgrades, setShowUpgrades] = useState(false);
  const [upgradeCategory, setUpgradeCategory] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;

  const renderUpgradeCategory = () => {
    switch (upgradeCategory) {
      case 'runners':
        return (
          <div>
            <h3>Runner Upgrades</h3>
            <Button onClick={() => game.upgradeRunnerSpeed()} cost={game.runnerSpeedCost} disabled={game.coinCount < game.runnerSpeedCost}>
              Upgrade Runner Speed
            </Button>
            <Button onClick={() => game.upgradeRunnerCount()} cost={game.runnerCountCost} disabled={game.coinCount < game.runnerCountCost}>
              Add Runner
            </Button>
          </div>
        );
      case 'tracks':
        return (
          <div>
            <h3>Track Upgrades</h3>
            <Button onClick={() => game.upgradeTrackCount()} cost={game.trackCountCost} disabled={game.coinCount < game.trackCountCost}>
              Add Track
            </Button>
          </div>
        );
      case 'coins':
        return (
          <div>
            <h3>Coin Upgrades</h3>
            <Button onClick={() => game.upgradeCoinValue()} cost={game.coinValueCost} disabled={game.coinCount < game.coinValueCost}>
              Increase Coin Value
            </Button>
            <Button onClick={() => game.upgradeCoinSpawnRate()} cost={game.coinSpawnRateCost} disabled={game.coinCount < game.coinSpawnRateCost}>
              Increase Coin Spawn Rate
            </Button>
            <Button onClick={() => game.upgradeCollisionRadius()} cost={game.collisionRadiusCost} disabled={game.coinCount < game.collisionRadiusCost}>
              Increase Collection Range
            </Button>
          </div>
        );
      default:
        return (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <MenuButton onClick={() => setUpgradeCategory('runners')}>Runner Upgrades</MenuButton>
            <MenuButton onClick={() => setUpgradeCategory('tracks')}>Track Upgrades</MenuButton>
            <MenuButton onClick={() => setUpgradeCategory('coins')}>Coin Upgrades</MenuButton>
          </div>
        );
    }
  };

  return (
    <div style={{ width: '100%', height: '100%', color: '#d3d3d3' }}>
      <HUD game={game} />
      
      <div style={{ position: 'absolute', bottom: '10px', right: '10px' }}>
        <MenuButton onClick={() => setShowStats(true)}>Stats</MenuButton>
        <MenuButton onClick={() => setShowUpgrades(true)}>Upgrades</MenuButton>
      </div>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Game Statistics">
        <div style={{ display: 'grid', gap: '10px' }}>
          <p>Runners: {game.runnerCount}</p>
          <p>Tracks: {game.trackCount}</p>
          <p>Runner Speed: {game.runnerSpeed.toFixed(1)}</p>
          <p>Coin Value: {game.coinValue.toFixed(1)}</p>
          <p>Coin Spawn Rate: {game.coinSpawnRate.toFixed(1)}/s</p>
          <p>Collection Range: {game.collisionRadius}</p>
        </div>
      </Modal>

      <Modal 
        isOpen={showUpgrades} 
        onClose={() => {
          setShowUpgrades(false);
          setUpgradeCategory(null);
        }} 
        title={upgradeCategory ? `Upgrades - ${upgradeCategory}` : 'Upgrades'}
      >
        {renderUpgradeCategory()}
        {upgradeCategory && (
          <button
            onClick={() => setUpgradeCategory(null)}
            style={{
              marginTop: '15px',
              padding: '5px 10px',
              background: 'none',
              border: '1px solid #7C45CB',
              color: '#d3d3d3',
              cursor: 'pointer'
            }}
          >
            Back
          </button>
        )}
      </Modal>
    </div>
  );
};

export default GameUI;
