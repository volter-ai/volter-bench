import React, { useState, useEffect } from 'react';
import { Coffee, Users, Settings, X, ChevronRight, Store, BarChart2 } from 'lucide-react';

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
      backdropFilter: 'blur(3px)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 100,
    }}>
      <div style={{
        backgroundColor: '#2A1810',
        border: '2px solid #8B4513',
        borderRadius: '10px',
        padding: '20px',
        width: '80%',
        maxWidth: '600px',
        maxHeight: '80%',
        overflow: 'auto',
        position: 'relative',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
        }}>
          <h2 style={{ margin: 0, color: '#E6B17E' }}>{title}</h2>
          <X 
            onClick={onClose}
            style={{ cursor: 'pointer', color: '#E6B17E' }}
          />
        </div>
        {children}
      </div>
    </div>
  );
};

const UpgradeCard = ({ title, cost, onClick, description }) => (
  <div style={{
    backgroundColor: '#3D2317',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '10px',
    border: '1px solid #8B4513',
  }}>
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    }}>
      <div>
        <h3 style={{ margin: '0 0 5px 0', color: '#E6B17E' }}>{title}</h3>
        <p style={{ margin: 0, fontSize: '14px', color: '#BFA08E' }}>{description}</p>
      </div>
      <button
        onClick={onClick}
        style={{
          backgroundColor: '#8B4513',
          color: '#E6B17E',
          border: 'none',
          padding: '8px 15px',
          borderRadius: '5px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '5px',
        }}
      >
        ${cost} <ChevronRight size={16} />
      </button>
    </div>
  </div>
);

const HUD = ({ money }) => (
  <div style={{
    position: 'absolute',
    top: '20px',
    left: '20px',
    backgroundColor: 'rgba(42, 24, 16, 0.9)',
    padding: '10px 20px',
    borderRadius: '25px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  }}>
    <Coffee size={20} color="#E6B17E" />
    <span style={{ color: '#E6B17E', fontWeight: 'bold' }}>${money}</span>
  </div>
);

const MenuButton = ({ icon: Icon, onClick }) => (
  <button
    onClick={onClick}
    style={{
      backgroundColor: 'rgba(42, 24, 16, 0.9)',
      border: 'none',
      borderRadius: '50%',
      width: '40px',
      height: '40px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      cursor: 'pointer',
      margin: '5px',
    }}
  >
    <Icon size={20} color="#E6B17E" />
  </button>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [showStats, setShowStats] = useState(false);
  const [showShop, setShowShop] = useState(false);
  const [activeShopTab, setActiveShopTab] = useState('staff');

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;
  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <HUD money={game.money} />
      
      <div style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        display: 'flex',
        flexDirection: 'column',
      }}>
        <MenuButton icon={BarChart2} onClick={() => setShowStats(true)} />
        <MenuButton icon={Store} onClick={() => setShowShop(true)} />
      </div>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Coffee Shop Stats">
        <div style={{ color: '#E6B17E' }}>
          <p>Baristas: {game.baristaCount}</p>
          <p>Coffee Price: ${game.coffeePrice}</p>
          <p>Customer Capacity: {game.customerCapacity}</p>
          <p>Barista Speed: {Math.round(game.baristaSpeed)}</p>
          <p>Coffee Make Time: {game.coffeeMakeTime.toFixed(1)}s</p>
        </div>
      </Modal>

      <Modal isOpen={showShop} onClose={() => setShowShop(false)} title="Coffee Shop Upgrades">
        <div style={{
          display: 'flex',
          gap: '10px',
          marginBottom: '20px',
        }}>
          {['staff', 'equipment', 'shop'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveShopTab(tab)}
              style={{
                backgroundColor: activeShopTab === tab ? '#8B4513' : '#3D2317',
                color: '#E6B17E',
                border: 'none',
                padding: '8px 15px',
                borderRadius: '5px',
                cursor: 'pointer',
                textTransform: 'capitalize',
              }}
            >
              {tab}
            </button>
          ))}
        </div>

        {activeShopTab === 'staff' && (
          <div>
            <UpgradeCard
              title="Hire Barista"
              cost={game.upgradeCosts.barista}
              onClick={() => game.upgradeBarista()}
              description="Hire an additional barista to serve more customers"
            />
            <UpgradeCard
              title="Upgrade Speed"
              cost={game.upgradeCosts.speed}
              onClick={() => game.upgradeSpeed()}
              description="Increase barista movement speed"
            />
          </div>
        )}

        {activeShopTab === 'equipment' && (
          <div>
            <UpgradeCard
              title="Coffee Machine Upgrade"
              cost={game.upgradeCosts.efficiency}
              onClick={() => game.upgradeEfficiency()}
              description="Reduce coffee preparation time"
            />
          </div>
        )}

        {activeShopTab === 'shop' && (
          <div>
            <UpgradeCard
              title="Increase Capacity"
              cost={game.upgradeCosts.capacity}
              onClick={() => game.upgradeCapacity()}
              description="Allow more customers in the shop"
            />
            <UpgradeCard
              title="Increase Coffee Price"
              cost={game.upgradeCosts.price}
              onClick={() => game.upgradePrice()}
              description="Charge more for each coffee"
            />
          </div>
        )}
      </Modal>
    </div>
  );
};

export default GameUI;
