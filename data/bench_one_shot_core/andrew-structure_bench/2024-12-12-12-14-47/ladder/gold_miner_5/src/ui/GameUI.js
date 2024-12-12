import React, { useState, useEffect } from 'react';
import { Settings, X, Users, Box, Cpu, Database, ChevronRight } from 'lucide-react';

const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  
  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.8)',
      backdropFilter: 'blur(4px)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000,
    }}>
      <div style={{
        backgroundColor: 'rgba(16, 24, 39, 0.95)',
        border: '1px solid #2563eb',
        borderRadius: '8px',
        padding: '20px',
        width: '80%',
        maxWidth: '600px',
        maxHeight: '80vh',
        overflow: 'auto',
        boxShadow: '0 0 20px rgba(37, 99, 235, 0.2)',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
        }}>
          <h2 style={{
            margin: 0,
            fontFamily: 'Orbitron',
            color: '#60a5fa',
            fontSize: '1.5rem',
          }}>{title}</h2>
          <X
            onClick={onClose}
            style={{ cursor: 'pointer', color: '#60a5fa' }}
          />
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
      color: disabled ? '#4b5563' : '#e5e7eb',
      border: 'none',
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: disabled ? '#1f2937' : '#3b82f6',
      borderRadius: '4px',
      fontFamily: 'Roboto',
      transition: 'all 0.2s',
      opacity: disabled ? 0.5 : 1,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      width: '100%',
    }}
  >
    <span>{children}</span>
    <span style={{
      backgroundColor: 'rgba(0,0,0,0.2)',
      padding: '2px 6px',
      borderRadius: '4px',
      fontSize: '12px',
    }}>{cost} 💎</span>
  </button>
);

const MenuButton = ({ onClick, icon: Icon, label }) => (
  <button
    onClick={onClick}
    style={{
      display: 'flex',
      alignItems: 'center',
      padding: '10px 15px',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      border: '1px solid #3b82f6',
      borderRadius: '4px',
      color: '#60a5fa',
      cursor: 'pointer',
      width: '100%',
      marginBottom: '10px',
      justifyContent: 'space-between',
    }}
  >
    <div style={{ display: 'flex', alignItems: 'center' }}>
      <Icon size={18} style={{ marginRight: '10px' }} />
      {label}
    </div>
    <ChevronRight size={18} />
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
    color: '#e5e7eb',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontFamily: 'Orbitron',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
      <span style={{ fontSize: '1.2rem' }}>
        💎 {Math.floor(game.crystals)}
      </span>
      <span>
        🤖 {game.droneCount}
      </span>
    </div>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [activeModal, setActiveModal] = useState(null);
  const [activeSubmenu, setActiveSubmenu] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;
  const game = gameRef.current;

  const renderSubmenu = () => {
    switch (activeSubmenu) {
      case 'drones':
        return (
          <>
            <Button 
              onClick={() => game.upgradeDroneCount()}
              cost={game.upgradeCosts.DRONE_COUNT}
              disabled={game.crystals < game.upgradeCosts.DRONE_COUNT}
            >
              Add Drone
            </Button>
            <Button 
              onClick={() => game.upgradeDroneSpeed()}
              cost={game.upgradeCosts.DRONE_SPEED}
              disabled={game.crystals < game.upgradeCosts.DRONE_SPEED}
            >
              Upgrade Drone Speed
            </Button>
          </>
        );
      case 'mining':
        return (
          <>
            <Button 
              onClick={() => game.upgradeCargoCapacity()}
              cost={game.upgradeCosts.CARGO_CAPACITY}
              disabled={game.crystals < game.upgradeCosts.CARGO_CAPACITY}
            >
              Upgrade Cargo Capacity
            </Button>
            <Button 
              onClick={() => game.upgradeMiningSpeed()}
              cost={game.upgradeCosts.MINING_SPEED}
              disabled={game.crystals < game.upgradeCosts.MINING_SPEED}
            >
              Upgrade Mining Speed
            </Button>
          </>
        );
      case 'resources':
        return (
          <>
            <Button 
              onClick={() => game.upgradeMaxAsteroids()}
              cost={game.upgradeCosts.MAX_ASTEROIDS}
              disabled={game.crystals < game.upgradeCosts.MAX_ASTEROIDS}
            >
              Increase Max Asteroids
            </Button>
            <Button 
              onClick={() => game.upgradeAsteroidCapacity()}
              cost={game.upgradeCosts.ASTEROID_CAPACITY}
              disabled={game.crystals < game.upgradeCosts.ASTEROID_CAPACITY}
            >
              Increase Asteroid Size
            </Button>
          </>
        );
      default:
        return (
          <>
            <MenuButton 
              onClick={() => setActiveSubmenu('drones')}
              icon={Users}
              label="Drone Management"
            />
            <MenuButton 
              onClick={() => setActiveSubmenu('mining')}
              icon={Cpu}
              label="Mining Operations"
            />
            <MenuButton 
              onClick={() => setActiveSubmenu('resources')}
              icon={Database}
              label="Resource Management"
            />
          </>
        );
    }
  };

  return (
    <div style={{ width: '100%', height: '100%', color: '#d3d3d3' }}>
      <HUD game={game} />
      
      <Settings
        onClick={() => setActiveModal('menu')}
        style={{
          position: 'absolute',
          bottom: '20px',
          right: '20px',
          cursor: 'pointer',
          color: '#60a5fa',
          backgroundColor: 'rgba(37, 99, 235, 0.1)',
          padding: '10px',
          borderRadius: '50%',
          border: '1px solid #3b82f6',
        }}
      />

      <Modal
        isOpen={activeModal === 'menu'}
        onClose={() => {
          setActiveModal(null);
          setActiveSubmenu(null);
        }}
        title={activeSubmenu ? `Upgrade ${activeSubmenu.charAt(0).toUpperCase() + activeSubmenu.slice(1)}` : "Station Control"}
      >
        {renderSubmenu()}
        {activeSubmenu && (
          <button
            onClick={() => setActiveSubmenu(null)}
            style={{
              marginTop: '20px',
              padding: '10px',
              backgroundColor: 'transparent',
              border: '1px solid #3b82f6',
              color: '#60a5fa',
              borderRadius: '4px',
              cursor: 'pointer',
              width: '100%',
            }}
          >
            Back to Main Menu
          </button>
        )}
      </Modal>
    </div>
  );
};

export default GameUI;
