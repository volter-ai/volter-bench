import React, { useState, useEffect } from 'react';
import { Settings, X, Users, Zap, Box, Database, Activity } from 'lucide-react';

const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  
  return (
    <div className="modal-backdrop" onClick={onClose} style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.85)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000
    }}>
      <div className="modal-content" onClick={e => e.stopPropagation()} style={{
        backgroundColor: '#1a1a2e',
        border: '2px solid #4a9eff',
        borderRadius: '10px',
        padding: '20px',
        minWidth: '300px',
        maxWidth: '500px',
        boxShadow: '0 0 20px rgba(74, 158, 255, 0.3)',
        color: '#fff'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ margin: 0, fontFamily: 'Orbitron', color: '#4a9eff' }}>{title}</h2>
          <X onClick={onClose} style={{ cursor: 'pointer', color: '#4a9eff' }} />
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
      fontSize: '14px',
      color: '#fff',
      border: '1px solid #4a9eff',
      borderRadius: '5px',
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: disabled ? '#1a1a2e' : '#2a2a4e',
      fontFamily: 'Roboto',
      transition: 'all 0.2s',
      opacity: disabled ? 0.5 : 1,
    }}
  >
    {children} ({cost} crystals)
  </button>
);

const IconButton = ({ onClick, icon: Icon, label }) => (
  <button
    onClick={onClick}
    style={{
      display: 'flex',
      alignItems: 'center',
      gap: '5px',
      padding: '8px 12px',
      backgroundColor: 'transparent',
      border: '1px solid #4a9eff',
      borderRadius: '5px',
      color: '#4a9eff',
      cursor: 'pointer',
      margin: '0 5px'
    }}
  >
    <Icon size={16} />
    {label}
  </button>
);

const HUD = ({ game }) => (
  <div style={{ 
    position: 'absolute', 
    top: 0, 
    left: 0, 
    right: 0, 
    padding: '15px', 
    background: 'linear-gradient(180deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 100%)',
    color: '#fff',
    fontFamily: 'Orbitron'
  }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span style={{ fontSize: '24px', color: '#4a9eff' }}>
        ⬢ {Math.floor(game.crystals)}
      </span>
      <div style={{ display: 'flex', gap: '10px' }}>
        <IconButton icon={Activity} label="Stats" onClick={() => game.setStatsOpen(true)} />
        <IconButton icon={Database} label="Upgrades" onClick={() => game.setUpgradesOpen(true)} />
      </div>
    </div>
  </div>
);

const StatsModal = ({ game, isOpen, onClose }) => (
  <Modal isOpen={isOpen} onClose={onClose} title="Station Statistics">
    <div style={{ fontFamily: 'Roboto' }}>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ color: '#4a9eff', fontFamily: 'Orbitron' }}>Drone Fleet</h3>
        <p>Active Drones: {game.droneCount}</p>
        <p>Speed Rating: {game.droneSpeed.toFixed(1)}</p>
        <p>Cargo Capacity: {game.droneCapacity}</p>
      </div>
      <div>
        <h3 style={{ color: '#4a9eff', fontFamily: 'Orbitron' }}>Asteroid Field</h3>
        <p>Maximum Asteroids: {game.maxAsteroids}</p>
        <p>Asteroid Capacity: {game.asteroidCapacity}</p>
      </div>
    </div>
  </Modal>
);

const UpgradeModal = ({ game, isOpen, onClose }) => {
  const [category, setCategory] = useState('drones');
  
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Station Upgrades">
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <IconButton 
          icon={Users} 
          label="Drones" 
          onClick={() => setCategory('drones')} 
        />
        <IconButton 
          icon={Box} 
          label="Cargo" 
          onClick={() => setCategory('cargo')} 
        />
        <IconButton 
          icon={Zap} 
          label="Field" 
          onClick={() => setCategory('field')} 
        />
      </div>
      
      <div style={{ display: category === 'drones' ? 'block' : 'none' }}>
        <Button onClick={() => game.upgradeDroneCount()} cost={game.droneCost}>
          Add Drone
        </Button>
        <Button onClick={() => game.upgradeDroneSpeed()} cost={game.speedCost}>
          Upgrade Speed
        </Button>
      </div>
      
      <div style={{ display: category === 'cargo' ? 'block' : 'none' }}>
        <Button onClick={() => game.upgradeDroneCapacity()} cost={game.capacityCost}>
          Upgrade Capacity
        </Button>
      </div>
      
      <div style={{ display: category === 'field' ? 'block' : 'none' }}>
        <Button onClick={() => game.upgradeMaxAsteroids()} cost={game.asteroidCountCost}>
          More Asteroids
        </Button>
        <Button onClick={() => game.upgradeAsteroidCapacity()} cost={game.asteroidCapacityCost}>
          Bigger Asteroids
        </Button>
      </div>
    </Modal>
  );
};

const GameUI = ({ gameRef }) => {
  const [statsOpen, setStatsOpen] = useState(false);
  const [upgradesOpen, setUpgradesOpen] = useState(false);
  const [, forceUpdate] = useState();

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;
  game.setStatsOpen = setStatsOpen;
  game.setUpgradesOpen = setUpgradesOpen;

  return (
    <div style={{ width: '100%', height: '100%', color: '#fff' }}>
      <HUD game={game} />
      <StatsModal 
        game={game} 
        isOpen={statsOpen} 
        onClose={() => setStatsOpen(false)} 
      />
      <UpgradeModal 
        game={game} 
        isOpen={upgradesOpen} 
        onClose={() => setUpgradesOpen(false)} 
      />
    </div>
  );
};

export default GameUI;
