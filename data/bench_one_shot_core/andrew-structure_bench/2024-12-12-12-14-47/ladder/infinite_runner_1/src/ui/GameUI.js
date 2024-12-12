import React, { useState, useEffect } from 'react';
import { Settings, X, Activity, ArrowUp, Layout } from 'lucide-react';

const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  
  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.7)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000,
    }}>
      <div style={{
        backgroundColor: '#1a1a2e',
        borderRadius: '8px',
        padding: '20px',
        minWidth: '300px',
        maxWidth: '600px',
        border: '1px solid #4a4a6a',
        boxShadow: '0 0 20px rgba(0,0,0,0.5)',
        color: '#fff',
        fontFamily: 'Roboto, sans-serif',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ margin: 0, fontFamily: 'Orbitron, sans-serif', color: '#00ff9d' }}>{title}</h2>
          <X onClick={onClose} style={{ cursor: 'pointer', color: '#888' }} />
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
      padding: '10px 15px',
      backgroundColor: disabled ? '#2a2a3e' : '#2a2a8e',
      border: 'none',
      borderRadius: '4px',
      color: disabled ? '#666' : 'white',
      cursor: disabled ? 'not-allowed' : 'pointer',
      fontFamily: 'Roboto, sans-serif',
      transition: 'all 0.2s',
      width: '100%',
      textAlign: 'left',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    }}
  >
    <span>{children}</span>
    <span style={{ 
      backgroundColor: disabled ? '#1a1a2e' : '#1a1a4e',
      padding: '4px 8px',
      borderRadius: '4px',
      fontSize: '0.9em'
    }}>
      {cost} coins
    </span>
  </button>
);

const HUD = ({ game }) => (
  <div style={{ 
    position: 'absolute', 
    top: '20px', 
    left: '20px', 
    padding: '10px 20px', 
    backgroundColor: 'rgba(26,26,46,0.9)', 
    color: '#00ff9d',
    borderRadius: '8px',
    fontFamily: 'Orbitron, sans-serif',
    fontSize: '1.2em',
    boxShadow: '0 0 10px rgba(0,255,157,0.2)',
  }}>
    <p style={{ margin: 0 }}>Score: {Math.floor(game.score)}</p>
  </div>
);

const MenuButton = ({ icon: Icon, onClick, style }) => (
  <button onClick={onClick} style={{
    backgroundColor: 'rgba(26,26,46,0.9)',
    border: 'none',
    borderRadius: '8px',
    padding: '10px',
    cursor: 'pointer',
    color: '#00ff9d',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.2s',
    ...style,
  }}>
    <Icon size={24} />
  </button>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [showStats, setShowStats] = useState(false);
  const [showUpgrades, setShowUpgrades] = useState(false);
  
  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;
  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%'}}>
      <HUD game={game} />
      
      <div style={{ 
        position: 'absolute', 
        top: '20px', 
        right: '20px',
        display: 'flex',
        gap: '10px',
      }}>
        <MenuButton icon={Activity} onClick={() => setShowStats(true)} />
        <MenuButton icon={ArrowUp} onClick={() => setShowUpgrades(true)} />
      </div>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Statistics">
        <div style={{ display: 'grid', gap: '10px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#2a2a3e', borderRadius: '4px' }}>
            <span>Runners</span>
            <span>{game.runnerCount}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#2a2a3e', borderRadius: '4px' }}>
            <span>Speed</span>
            <span>{game.runnerSpeed.toFixed(1)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#2a2a3e', borderRadius: '4px' }}>
            <span>Coin Value</span>
            <span>{game.coinValue.toFixed(1)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#2a2a3e', borderRadius: '4px' }}>
            <span>Spawn Rate</span>
            <span>{game.coinSpawnRate.toFixed(1)}/s</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#2a2a3e', borderRadius: '4px' }}>
            <span>Track Width</span>
            <span>{Math.floor(game.trackWidth)}</span>
          </div>
        </div>
      </Modal>

      <Modal isOpen={showUpgrades} onClose={() => setShowUpgrades(false)} title="Upgrades">
        <div style={{ display: 'grid', gap: '15px' }}>
          <div>
            <h3 style={{ color: '#00ff9d', fontFamily: 'Orbitron, sans-serif', fontSize: '1em', marginBottom: '10px' }}>Runner Upgrades</h3>
            <Button onClick={() => game.upgradeRunnerSpeed()} cost={game.runnerSpeedCost} disabled={game.score < game.runnerSpeedCost}>
              Upgrade Runner Speed
            </Button>
            <Button onClick={() => game.upgradeRunnerCount()} cost={game.runnerCountCost} disabled={game.score < game.runnerCountCost}>
              Add Runner
            </Button>
          </div>
          
          <div>
            <h3 style={{ color: '#00ff9d', fontFamily: 'Orbitron, sans-serif', fontSize: '1em', marginBottom: '10px' }}>Economy Upgrades</h3>
            <Button onClick={() => game.upgradeCoinSpawnRate()} cost={game.coinSpawnRateCost} disabled={game.score < game.coinSpawnRateCost}>
              Upgrade Spawn Rate
            </Button>
            <Button onClick={() => game.upgradeCoinValue()} cost={game.coinValueCost} disabled={game.score < game.coinValueCost}>
              Upgrade Coin Value
            </Button>
          </div>
          
          <div>
            <h3 style={{ color: '#00ff9d', fontFamily: 'Orbitron, sans-serif', fontSize: '1em', marginBottom: '10px' }}>Track Upgrades</h3>
            <Button onClick={() => game.upgradeTrackWidth()} cost={game.trackWidthCost} disabled={game.score < game.trackWidthCost}>
              Expand Track
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default GameUI;
