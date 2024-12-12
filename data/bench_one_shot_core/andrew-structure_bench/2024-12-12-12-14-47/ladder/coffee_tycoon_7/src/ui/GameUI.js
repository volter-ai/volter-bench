import React, { useState, useEffect } from 'react';
import { Coffee, Users, Settings, TrendingUp, Package, Award } from 'lucide-react';

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
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: '#2A1810',
        padding: '20px',
        borderRadius: '10px',
        minWidth: '300px',
        maxWidth: '500px',
        border: '2px solid #8B4513',
        boxShadow: '0 0 20px rgba(0,0,0,0.5)'
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
            color: '#D2691E'
          }}>{title}</h2>
          <button onClick={onClose} style={{
            background: 'none',
            border: 'none',
            color: '#D2691E',
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
      padding: '10px 15px',
      fontSize: '14px',
      color: disabled ? '#666' : '#FFF8DC',
      border: 'none',
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: disabled ? '#4A3228' : '#8B4513',
      borderRadius: '5px',
      fontFamily: 'Roboto',
      transition: 'all 0.2s',
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      width: '100%'
    }}>
    {children} {cost && <span style={{marginLeft: 'auto'}}>${cost}</span>}
  </button>
);

const MenuButton = ({ onClick, children, icon: Icon }) => (
  <button
    onClick={onClick}
    style={{
      padding: '10px',
      backgroundColor: '#2A1810',
      border: '2px solid #8B4513',
      borderRadius: '5px',
      color: '#D2691E',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '5px',
      margin: '0 5px'
    }}>
    <Icon size={16} />
    {children}
  </button>
);

const HUD = ({ game }) => (
  <div style={{
    position: 'absolute',
    top: '10px',
    left: '10px',
    padding: '10px 20px',
    backgroundColor: 'rgba(42, 24, 16, 0.9)',
    color: '#D2691E',
    borderRadius: '5px',
    fontFamily: 'Orbitron',
    display: 'flex',
    gap: '20px',
    alignItems: 'center'
  }}>
    <Coffee size={20} />
    <span>${Math.floor(game.money)}</span>
    <Users size={20} />
    <span>{game.customers ? game.customers.children.length : 0}/{game.maxCustomers}</span>
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

  if (!gameRef.current || !gameRef.current.ready) return null;

  const game = gameRef.current;

  const renderUpgradeCategory = () => {
    switch (upgradeCategory) {
      case 'staff':
        return (
          <div>
            <h3 style={{color: '#D2691E', fontFamily: 'Orbitron'}}>Staff Management</h3>
            <Button onClick={() => game.upgradeBaristas()} cost={game.upgradeCosts.barista}>
              <Users size={16} /> Hire Barista
            </Button>
            <Button onClick={() => game.upgradeSpeed()} cost={game.upgradeCosts.speed}>
              <TrendingUp size={16} /> Train Baristas
            </Button>
          </div>
        );
      case 'equipment':
        return (
          <div>
            <h3 style={{color: '#D2691E', fontFamily: 'Orbitron'}}>Equipment</h3>
            <Button onClick={() => game.upgradeMachines()} cost={game.upgradeCosts.machine}>
              <Coffee size={16} /> New Machine
            </Button>
            <Button onClick={() => game.upgradeQuality()} cost={game.upgradeCosts.quality}>
              <Award size={16} /> Better Coffee
            </Button>
          </div>
        );
      case 'business':
        return (
          <div>
            <h3 style={{color: '#D2691E', fontFamily: 'Orbitron'}}>Business</h3>
            <Button onClick={() => game.upgradeSpace()} cost={game.upgradeCosts.space}>
              <Package size={16} /> Expand Shop
            </Button>
          </div>
        );
      default:
        return (
          <div style={{display: 'flex', flexDirection: 'column', gap: '10px'}}>
            <Button onClick={() => setUpgradeCategory('staff')}>Staff Management</Button>
            <Button onClick={() => setUpgradeCategory('equipment')}>Equipment</Button>
            <Button onClick={() => setUpgradeCategory('business')}>Business</Button>
          </div>
        );
    }
  };

  return (
    <div style={{ width: '100%', height: '100%', color: '#D2691E' }}>
      <HUD game={game} />
      
      <div style={{
        position: 'absolute',
        bottom: '10px',
        left: '10px',
        display: 'flex',
        gap: '10px'
      }}>
        <MenuButton onClick={() => setShowStats(true)} icon={TrendingUp}>
          Stats
        </MenuButton>
        <MenuButton onClick={() => {
          setShowUpgrades(true);
          setUpgradeCategory(null);
        }} icon={Coffee}>
          Upgrades
        </MenuButton>
      </div>

      <Modal
        isOpen={showStats}
        onClose={() => setShowStats(false)}
        title="Business Statistics"
      >
        <div style={{color: '#D2691E', fontFamily: 'Roboto'}}>
          <p>Baristas: {game.baristaCount}</p>
          <p>Machines: {game.machineCount}</p>
          <p>Shop Capacity: {game.maxCustomers}</p>
          <p>Coffee Quality: {Math.floor(game.coffeeQuality * 100)}%</p>
          <p>Service Speed: {Math.floor(game.baristaSpeed)}%</p>
        </div>
      </Modal>

      <Modal
        isOpen={showUpgrades}
        onClose={() => {
          setShowUpgrades(false);
          setUpgradeCategory(null);
        }}
        title={upgradeCategory ? 'Upgrades' : 'Select Category'}
      >
        {renderUpgradeCategory()}
      </Modal>
    </div>
  );
};

export default GameUI;
