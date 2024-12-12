import React, { useState, useEffect } from 'react';
import { ChevronLeft, X, Users, Coffee, DollarSign, BarChart2, Store } from 'lucide-react';

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
      zIndex: 100,
      animation: 'fadeIn 0.2s ease-out'
    }}>
      <div style={{
        backgroundColor: '#1a1a2e',
        border: '1px solid #7C45CB',
        borderRadius: '8px',
        padding: '20px',
        width: '80%',
        maxWidth: '600px',
        maxHeight: '80%',
        overflow: 'auto',
        position: 'relative',
        boxShadow: '0 0 20px rgba(124, 69, 203, 0.3)',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
          borderBottom: '1px solid #7C45CB',
          paddingBottom: '10px'
        }}>
          <h2 style={{ 
            margin: 0, 
            fontFamily: 'Orbitron',
            color: '#fff',
            fontSize: '1.5em'
          }}>{title}</h2>
          <X
            onClick={onClose}
            style={{
              cursor: 'pointer',
              color: '#7C45CB',
              transition: 'color 0.2s',
            }}
            onMouseOver={e => e.target.style.color = '#9b6ae0'}
            onMouseOut={e => e.target.style.color = '#7C45CB'}
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
      margin: '10px',
      padding: '12px 20px',
      fontSize: '14px',
      color: '#fff',
      border: '1px solid #7C45CB',
      borderRadius: '4px',
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: disabled ? '#2a2a3e' : '#1a1a2e',
      fontFamily: 'Orbitron',
      transition: 'all 0.2s',
      opacity: disabled ? 0.6 : 1,
      width: '100%',
      textAlign: 'left',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    }}
  >
    <span>{children}</span>
    <span style={{
      backgroundColor: '#7C45CB',
      padding: '4px 8px',
      borderRadius: '4px',
      fontSize: '0.9em'
    }}>${cost}</span>
  </button>
);

const HUD = ({ game, onOpenStats, onOpenUpgrades }) => (
  <div style={{
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    padding: '15px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    background: 'linear-gradient(180deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 100%)',
  }}>
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      color: '#fff',
      fontFamily: 'Orbitron',
    }}>
      <DollarSign size={20} color="#7C45CB" />
      <span style={{ fontSize: '1.2em' }}>{Math.floor(game.money)}</span>
    </div>
    <div style={{ display: 'flex', gap: '15px' }}>
      <BarChart2
        size={24}
        color="#7C45CB"
        style={{ cursor: 'pointer' }}
        onClick={onOpenStats}
      />
      <Store
        size={24}
        color="#7C45CB"
        style={{ cursor: 'pointer' }}
        onClick={onOpenUpgrades}
      />
    </div>
  </div>
);

const StatsModal = ({ game, isOpen, onClose }) => (
  <Modal isOpen={isOpen} onClose={onClose} title="Statistics">
    <div style={{
      display: 'grid',
      gap: '15px',
      color: '#fff',
      fontFamily: 'Orbitron',
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#2a2a3e', borderRadius: '4px' }}>
        <span>Baristas</span>
        <span>{game.baristaCount}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#2a2a3e', borderRadius: '4px' }}>
        <span>Counters</span>
        <span>{game.counterCount}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#2a2a3e', borderRadius: '4px' }}>
        <span>Coffee Price</span>
        <span>${game.paymentAmount}</span>
      </div>
    </div>
  </Modal>
);

const UpgradesModal = ({ game, isOpen, onClose }) => {
  const [category, setCategory] = useState(null);

  const renderCategoryContent = () => {
    switch(category) {
      case 'staff':
        return (
          <div>
            <Button onClick={() => game.upgradeBaristas()} cost={game.upgradeCosts.BARISTA}>
              Hire Barista
            </Button>
            <Button onClick={() => game.upgradeBaristaSpeed()} cost={game.upgradeCosts.BARISTA_SPEED}>
              Faster Baristas
            </Button>
            <Button onClick={() => game.upgradeTraining()} cost={game.upgradeCosts.TRAINING}>
              Efficient Training
            </Button>
          </div>
        );
      case 'equipment':
        return (
          <div>
            <Button onClick={() => game.upgradeCoffeeMachine()} cost={game.upgradeCosts.COFFEE_MACHINE}>
              Better Machines
            </Button>
            <Button onClick={() => game.upgradeCounter()} cost={game.upgradeCosts.COUNTER}>
              Add Counter
            </Button>
          </div>
        );
      case 'business':
        return (
          <div>
            <Button onClick={() => game.upgradePrices()} cost={game.upgradeCosts.PREMIUM_PRICES}>
              Premium Prices
            </Button>
          </div>
        );
      default:
        return (
          <div style={{
            display: 'grid',
            gap: '15px',
            gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          }}>
            {['staff', 'equipment', 'business'].map(cat => (
              <div
                key={cat}
                onClick={() => setCategory(cat)}
                style={{
                  padding: '20px',
                  backgroundColor: '#2a2a3e',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  textAlign: 'center',
                  color: '#fff',
                  fontFamily: 'Orbitron',
                  border: '1px solid #7C45CB',
                  transition: 'all 0.2s',
                }}
                onMouseOver={e => e.currentTarget.style.transform = 'scale(1.05)'}
                onMouseOut={e => e.currentTarget.style.transform = 'scale(1)'}
              >
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </div>
            ))}
          </div>
        );
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={category ? `Upgrades - ${category.charAt(0).toUpperCase() + category.slice(1)}` : 'Upgrades'}>
      {category && (
        <div
          onClick={() => setCategory(null)}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '5px',
            color: '#7C45CB',
            cursor: 'pointer',
            marginBottom: '20px',
          }}
        >
          <ChevronLeft size={20} />
          <span>Back</span>
        </div>
      )}
      {renderCategoryContent()}
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
      <HUD
        game={game}
        onOpenStats={() => setShowStats(true)}
        onOpenUpgrades={() => setShowUpgrades(true)}
      />
      <StatsModal
        game={game}
        isOpen={showStats}
        onClose={() => setShowStats(false)}
      />
      <UpgradesModal
        game={game}
        isOpen={showUpgrades}
        onClose={() => setShowUpgrades(false)}
      />
    </div>
  );
};

export default GameUI;
