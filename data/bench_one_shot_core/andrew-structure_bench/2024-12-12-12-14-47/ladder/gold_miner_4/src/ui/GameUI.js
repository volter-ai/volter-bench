import React, { useState, useEffect } from 'react';
import { Settings, Plus, Box, Rocket, Activity } from 'lucide-react';

const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  
  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.8)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: '#1a1a2e',
        border: '2px solid #00fff2',
        borderRadius: '8px',
        padding: '20px',
        minWidth: '300px',
        boxShadow: '0 0 20px rgba(0,255,242,0.3)',
        color: 'white'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px'
        }}>
          <h2 style={{ 
            margin: 0,
            fontFamily: 'Orbitron',
            color: '#00fff2'
          }}>{title}</h2>
          <button onClick={onClose} style={{
            background: 'none',
            border: 'none',
            color: '#00fff2',
            cursor: 'pointer',
            fontSize: '20px'
          }}>×</button>
        </div>
        {children}
      </div>
    </div>
  );
};

const Button = ({ onClick, children, cost, disabled, icon: Icon }) => (
  <button 
    onClick={onClick} 
    disabled={disabled}
    style={{
      margin: '5px',
      padding: '10px 15px',
      fontSize: '14px',
      backgroundColor: disabled ? '#1a1a2e' : '#16213e',
      color: disabled ? '#4a4a6a' : '#00fff2',
      border: `1px solid ${disabled ? '#4a4a6a' : '#00fff2'}`,
      borderRadius: '4px',
      cursor: disabled ? 'default' : 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      fontFamily: 'Roboto',
      transition: 'all 0.2s'
    }}
  >
    {Icon && <Icon size={16} />}
    <span>{children}</span>
    <span style={{ opacity: 0.8 }}>({cost})</span>
  </button>
);

const HUD = ({ game }) => (
  <div style={{ 
    position: 'absolute', 
    top: '20px', 
    left: '20px', 
    padding: '10px 20px', 
    backgroundColor: 'rgba(26,26,46,0.9)',
    borderRadius: '8px',
    border: '1px solid #00fff2',
    color: 'white',
    fontFamily: 'Orbitron'
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      <Box size={16} color="#00fff2" />
      <span style={{ color: '#00fff2' }}>{Math.floor(game.crystals)}</span>
      <span>crystals</span>
    </div>
  </div>
);

const StatsModal = ({ game, isOpen, onClose }) => (
  <Modal isOpen={isOpen} onClose={onClose} title="Station Statistics">
    <div style={{ fontFamily: 'Roboto' }}>
      <div style={{ marginBottom: '15px' }}>
        <h3 style={{ color: '#00fff2', fontFamily: 'Orbitron' }}>Drone Fleet</h3>
        <p>Count: {game.droneCount}</p>
        <p>Speed: {game.droneSpeed.toFixed(1)}</p>
        <p>Cargo Capacity: {Math.floor(game.droneCargo)}</p>
      </div>
      <div>
        <h3 style={{ color: '#00fff2', fontFamily: 'Orbitron' }}>Asteroid Field</h3>
        <p>Capacity per Asteroid: {Math.floor(game.asteroidCapacity)}</p>
        <p>Maximum Asteroids: {game.maxAsteroids}</p>
      </div>
    </div>
  </Modal>
);

const UpgradeModal = ({ game, isOpen, onClose }) => {
  const [category, setCategory] = useState(null);
  
  const renderCategory = () => {
    if (!category) {
      return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <Button onClick={() => setCategory('drones')} icon={Rocket}>
            Drone Management
          </Button>
          <Button onClick={() => setCategory('asteroids')} icon={Box}>
            Asteroid Management
          </Button>
        </div>
      );
    }

    if (category === 'drones') {
      return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <Button 
            onClick={() => game.upgradeDroneCount()} 
            cost={game.droneCountCost}
            disabled={game.crystals < game.droneCountCost}
          >
            Add Drone
          </Button>
          <Button 
            onClick={() => game.upgradeDroneSpeed()} 
            cost={game.droneSpeedCost}
            disabled={game.crystals < game.droneSpeedCost}
          >
            Upgrade Speed
          </Button>
          <Button 
            onClick={() => game.upgradeDroneCargo()} 
            cost={game.droneCargoCost}
            disabled={game.crystals < game.droneCargoCost}
          >
            Upgrade Cargo
          </Button>
          <Button onClick={() => setCategory(null)}>Back</Button>
        </div>
      );
    }

    if (category === 'asteroids') {
      return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <Button 
            onClick={() => game.upgradeAsteroidCapacity()} 
            cost={game.asteroidCapacityCost}
            disabled={game.crystals < game.asteroidCapacityCost}
          >
            Upgrade Capacity
          </Button>
          <Button 
            onClick={() => game.upgradeMaxAsteroids()} 
            cost={game.maxAsteroidsCost}
            disabled={game.crystals < game.maxAsteroidsCost}
          >
            Add Asteroid
          </Button>
          <Button onClick={() => setCategory(null)}>Back</Button>
        </div>
      );
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Upgrades">
      {renderCategory()}
    </Modal>
  );
};

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
    <div style={{ width: '100%', height: '100%' }}>
      <HUD game={game} />
      
      <div style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        display: 'flex',
        gap: '10px'
      }}>
        <Button onClick={() => setShowStats(true)} icon={Activity}>
          Stats
        </Button>
        <Button onClick={() => setShowUpgrades(true)} icon={Plus}>
          Upgrades
        </Button>
      </div>

      <StatsModal 
        game={game} 
        isOpen={showStats} 
        onClose={() => setShowStats(false)} 
      />
      
      <UpgradeModal 
        game={game} 
        isOpen={showUpgrades} 
        onClose={() => setShowUpgrades(false)} 
      />
    </div>
  );
};

export default GameUI;
