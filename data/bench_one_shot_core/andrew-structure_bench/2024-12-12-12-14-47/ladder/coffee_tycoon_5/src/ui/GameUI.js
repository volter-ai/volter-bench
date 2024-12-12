import React, { useState, useEffect } from 'react';
import { Coffee, Users, Settings, DollarSign, Timer, ShoppingBag, BarChart2, X } from 'lucide-react';

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
        backgroundColor: '#1a1a1a',
        padding: '20px',
        borderRadius: '10px',
        minWidth: '400px',
        border: '1px solid #3a3a3a',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        position: 'relative'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px'
        }}>
          <h2 style={{ margin: 0, fontFamily: 'Orbitron', color: '#e0e0e0' }}>{title}</h2>
          <X 
            onClick={onClose}
            style={{ cursor: 'pointer', color: '#888' }}
          />
        </div>
        {children}
      </div>
    </div>
  );
};

const Button = ({ onClick, children, cost, icon: Icon }) => (
  <button onClick={onClick} style={{
    margin: '5px',
    padding: '10px 15px',
    fontSize: '14px',
    color: '#e0e0e0',
    border: 'none',
    cursor: 'pointer',
    backgroundColor: '#2a2a2a',
    borderRadius: '5px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    width: '100%',
    transition: 'background-color 0.2s',
    fontFamily: 'Orbitron',
    ':hover': {
      backgroundColor: '#3a3a3a'
    }
  }}>
    {Icon && <Icon size={16} />}
    <span style={{ flex: 1, textAlign: 'left' }}>{children}</span>
    <span style={{ color: '#ffd700' }}>${cost}</span>
  </button>
);

const HUD = ({ game }) => (
  <div style={{
    position: 'absolute',
    top: '20px',
    left: '20px',
    padding: '15px',
    backgroundColor: 'rgba(0,0,0,0.7)',
    color: '#e0e0e0',
    borderRadius: '10px',
    fontFamily: 'Orbitron',
    display: 'flex',
    alignItems: 'center',
    gap: '10px'
  }}>
    <DollarSign size={20} color="#ffd700" />
    <span style={{ fontSize: '20px' }}>{Math.floor(game.money)}</span>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [showShop, setShowShop] = useState(false);
  const [showStats, setShowStats] = useState(false);
  const [activeShopTab, setActiveShopTab] = useState('staff');

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;
  const game = gameRef.current;

  const renderShopContent = () => {
    switch (activeShopTab) {
      case 'staff':
        return (
          <div>
            <Button icon={Users} onClick={() => game.upgradeBaristaCount()} cost={game.baristaCountCost}>
              Hire Barista
            </Button>
            <Button icon={Timer} onClick={() => game.upgradeBaristaSpeed()} cost={game.baristaSpeedCost}>
              Upgrade Barista Speed
            </Button>
          </div>
        );
      case 'equipment':
        return (
          <div>
            <Button icon={Coffee} onClick={() => game.upgradeCoffeeMachine()} cost={game.coffeeMachineCost}>
              Upgrade Coffee Machines
            </Button>
            <Button icon={ShoppingBag} onClick={() => game.upgradeCounterCount()} cost={game.counterCountCost}>
              Add Counter
            </Button>
          </div>
        );
      case 'business':
        return (
          <div>
            <Button icon={DollarSign} onClick={() => game.upgradeCoffeePrice()} cost={game.coffeePriceCost}>
              Increase Coffee Price
            </Button>
            <Button icon={Users} onClick={() => game.upgradeCustomerAttraction()} cost={game.customerAttractionCost}>
              Improve Customer Attraction
            </Button>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div style={{ width: '100%', height: '100%', color: '#e0e0e0' }}>
      <HUD game={game} />
      
      <div style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        display: 'flex',
        gap: '10px'
      }}>
        <button onClick={() => setShowShop(true)} style={{
          padding: '10px',
          backgroundColor: '#2a2a2a',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}>
          <ShoppingBag color="#e0e0e0" />
        </button>
        <button onClick={() => setShowStats(true)} style={{
          padding: '10px',
          backgroundColor: '#2a2a2a',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}>
          <BarChart2 color="#e0e0e0" />
        </button>
      </div>

      <Modal isOpen={showShop} onClose={() => setShowShop(false)} title="Shop">
        <div style={{ display: 'flex', gap: '20px' }}>
          <div style={{ width: '150px', borderRight: '1px solid #3a3a3a', paddingRight: '20px' }}>
            <button
              onClick={() => setActiveShopTab('staff')}
              style={{
                width: '100%',
                padding: '10px',
                backgroundColor: activeShopTab === 'staff' ? '#3a3a3a' : 'transparent',
                border: 'none',
                color: '#e0e0e0',
                textAlign: 'left',
                cursor: 'pointer',
                marginBottom: '10px'
              }}
            >
              Staff
            </button>
            <button
              onClick={() => setActiveShopTab('equipment')}
              style={{
                width: '100%',
                padding: '10px',
                backgroundColor: activeShopTab === 'equipment' ? '#3a3a3a' : 'transparent',
                border: 'none',
                color: '#e0e0e0',
                textAlign: 'left',
                cursor: 'pointer',
                marginBottom: '10px'
              }}
            >
              Equipment
            </button>
            <button
              onClick={() => setActiveShopTab('business')}
              style={{
                width: '100%',
                padding: '10px',
                backgroundColor: activeShopTab === 'business' ? '#3a3a3a' : 'transparent',
                border: 'none',
                color: '#e0e0e0',
                textAlign: 'left',
                cursor: 'pointer'
              }}
            >
              Business
            </button>
          </div>
          <div style={{ flex: 1 }}>
            {renderShopContent()}
          </div>
        </div>
      </Modal>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Statistics">
        <div style={{ color: '#e0e0e0', fontFamily: 'Orbitron' }}>
          <div style={{ marginBottom: '15px', padding: '10px', backgroundColor: '#2a2a2a', borderRadius: '5px' }}>
            <p>Baristas: {game.baristaCount}</p>
            <p>Coffee Price: ${game.coffeePrice.toFixed(2)}</p>
            <p>Customer Spawn Rate: {game.customerSpawnTime.toFixed(1)}s</p>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default GameUI;
