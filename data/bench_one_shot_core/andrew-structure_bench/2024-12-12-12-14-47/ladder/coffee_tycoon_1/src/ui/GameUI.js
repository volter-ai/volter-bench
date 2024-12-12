import React, { useState, useEffect } from 'react';
import { Coffee, Users, Settings, DollarSign, ChevronRight, X, Activity } from 'lucide-react';

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
        backgroundColor: '#2A1810',
        padding: '20px',
        borderRadius: '10px',
        minWidth: '300px',
        border: '2px solid #8B4513',
        boxShadow: '0 0 20px rgba(0,0,0,0.5)',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
        }}>
          <h2 style={{ margin: 0, color: '#D2691E', fontFamily: 'Orbitron' }}>{title}</h2>
          <X onClick={onClose} style={{ cursor: 'pointer', color: '#D2691E' }} />
        </div>
        {children}
      </div>
    </div>
  );
};

const Button = ({ onClick, children, cost, icon: Icon }) => (
  <button onClick={onClick} style={{
    margin: '8px',
    padding: '10px 15px',
    fontSize: '14px',
    color: '#FFF8DC',
    border: '2px solid #8B4513',
    borderRadius: '5px',
    cursor: 'pointer',
    backgroundColor: '#3C1810',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    transition: 'all 0.2s',
    fontFamily: 'Orbitron',
    width: '100%',
  }}>
    {Icon && <Icon size={18} />}
    <span style={{ flex: 1 }}>{children}</span>
    {cost && <span>${cost}</span>}
  </button>
);

const HUD = ({ game }) => (
  <div style={{
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    padding: '15px',
    background: 'linear-gradient(to bottom, rgba(42,24,16,0.9) 0%, rgba(42,24,16,0.7) 100%)',
    color: '#FFF8DC',
    fontFamily: 'Orbitron',
    display: 'flex',
    alignItems: 'center',
    gap: '20px',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
      <DollarSign size={18} />
      <span>{Math.floor(game.money)}</span>
    </div>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [showStats, setShowStats] = useState(false);
  const [showUpgrades, setShowUpgrades] = useState(false);
  const [upgradeCategory, setUpgradeCategory] = useState('staff');

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;
  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%', color: '#FFF8DC' }}>
      <HUD game={game} />
      
      <div style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        display: 'flex',
        gap: '10px',
      }}>
        <Button icon={Activity} onClick={() => setShowStats(true)}>Stats</Button>
        <Button icon={Coffee} onClick={() => setShowUpgrades(true)}>Upgrades</Button>
      </div>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Statistics">
        <div style={{ color: '#FFF8DC' }}>
          <p>Baristas: {game.baristaCount}</p>
          <p>Barista Speed: {game.baristaSpeed.toFixed(1)}x</p>
          <p>Brew Time: {game.brewTime.toFixed(1)}s</p>
          <p>Max Customers: {game.maxCustomers}</p>
          <p>Coffee Price: ${game.coffeePrice.toFixed(2)}</p>
        </div>
      </Modal>

      <Modal isOpen={showUpgrades} onClose={() => setShowUpgrades(false)} title="Upgrades">
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          <Button onClick={() => setUpgradeCategory('staff')} 
                  style={{ backgroundColor: upgradeCategory === 'staff' ? '#8B4513' : '#3C1810' }}>
            Staff
          </Button>
          <Button onClick={() => setUpgradeCategory('equipment')}
                  style={{ backgroundColor: upgradeCategory === 'equipment' ? '#8B4513' : '#3C1810' }}>
            Equipment
          </Button>
          <Button onClick={() => setUpgradeCategory('business')}
                  style={{ backgroundColor: upgradeCategory === 'business' ? '#8B4513' : '#3C1810' }}>
            Business
          </Button>
        </div>

        {upgradeCategory === 'staff' && (
          <div>
            <Button icon={Users} onClick={() => game.upgradeBarista()} cost={Math.floor(game.baristaCost)}>
              Hire Barista
            </Button>
            <Button icon={ChevronRight} onClick={() => game.upgradeBaristaSpeed()} cost={Math.floor(game.baristaSpeedCost)}>
              Upgrade Barista Speed
            </Button>
          </div>
        )}

        {upgradeCategory === 'equipment' && (
          <div>
            <Button icon={Coffee} onClick={() => game.upgradeBrewSpeed()} cost={Math.floor(game.brewSpeedCost)}>
              Upgrade Brewing Speed
            </Button>
          </div>
        )}

        {upgradeCategory === 'business' && (
          <div>
            <Button icon={Users} onClick={() => game.upgradeMaxCustomers()} cost={Math.floor(game.maxCustomersCost)}>
              Increase Customer Capacity
            </Button>
            <Button icon={DollarSign} onClick={() => game.upgradeCoffeePrice()} cost={Math.floor(game.priceCost)}>
              Increase Coffee Price
            </Button>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default GameUI;
