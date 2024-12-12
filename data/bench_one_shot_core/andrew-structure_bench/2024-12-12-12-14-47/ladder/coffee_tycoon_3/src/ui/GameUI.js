import React, { useState, useEffect } from 'react';
import { Coffee, Users, DollarSign, ChevronRight, X, BarChart2, UserPlus, Coffee as CoffeeIcon, Users as CustomersIcon } from 'lucide-react';

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
      backdropFilter: 'blur(3px)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000,
    }}>
      <div style={{
        backgroundColor: '#2C1810',
        padding: '20px',
        borderRadius: '10px',
        minWidth: '300px',
        maxWidth: '500px',
        border: '1px solid #D4A574',
        color: '#F5E6D3',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ margin: 0, fontFamily: 'Orbitron' }}>{title}</h2>
          <X onClick={onClose} style={{ cursor: 'pointer', color: '#D4A574' }} />
        </div>
        {children}
      </div>
    </div>
  );
};

const Button = ({ onClick, children, cost, icon: Icon }) => (
  <button onClick={onClick} style={{
    margin: '10px',
    padding: '10px 15px',
    fontSize: '14px',
    color: '#F5E6D3',
    border: '1px solid #D4A574',
    borderRadius: '5px',
    cursor: 'pointer',
    backgroundColor: '#2C1810',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    width: '100%',
    transition: 'all 0.2s',
    fontFamily: 'Orbitron',
  }}>
    {Icon && <Icon size={16} />}
    <span style={{ flex: 1, textAlign: 'left' }}>{children}</span>
    <span style={{ color: '#D4A574' }}>${cost}</span>
  </button>
);

const MenuButton = ({ onClick, children, icon: Icon }) => (
  <button onClick={onClick} style={{
    padding: '10px 15px',
    margin: '5px',
    backgroundColor: '#2C1810',
    border: '1px solid #D4A574',
    borderRadius: '5px',
    color: '#F5E6D3',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    fontFamily: 'Orbitron',
  }}>
    {Icon && <Icon size={16} />}
    {children}
    <ChevronRight size={16} />
  </button>
);

const HUD = ({ game }) => (
  <div style={{
    position: 'absolute',
    top: '20px',
    left: '20px',
    padding: '15px',
    backgroundColor: 'rgba(44, 24, 16, 0.9)',
    color: '#F5E6D3',
    borderRadius: '10px',
    border: '1px solid #D4A574',
    fontFamily: 'Orbitron',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      <DollarSign size={16} color="#D4A574" />
      <span style={{ fontSize: '18px' }}>{Math.floor(game.money)}</span>
    </div>
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '5px' }}>
      <Coffee size={16} color="#D4A574" />
      <span>${game.coffeePrice.toFixed(2)}</span>
    </div>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [activeModal, setActiveModal] = useState(null);
  
  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;
  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%', color: '#F5E6D3' }}>
      <HUD game={game} />
      
      <div style={{ position: 'absolute', bottom: '20px', right: '20px' }}>
        <MenuButton onClick={() => setActiveModal('main')} icon={Coffee}>Menu</MenuButton>
      </div>

      <Modal isOpen={activeModal === 'main'} onClose={() => setActiveModal(null)} title="Management Menu">
        <MenuButton onClick={() => setActiveModal('stats')} icon={BarChart2}>Statistics</MenuButton>
        <MenuButton onClick={() => setActiveModal('staff')} icon={UserPlus}>Staff Management</MenuButton>
        <MenuButton onClick={() => setActiveModal('product')} icon={CoffeeIcon}>Product Management</MenuButton>
        <MenuButton onClick={() => setActiveModal('customer')} icon={CustomersIcon}>Customer Service</MenuButton>
      </Modal>

      <Modal isOpen={activeModal === 'stats'} onClose={() => setActiveModal('main')} title="Statistics">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <p>Coffee Make Speed: {game.coffeeMakeSpeed.toFixed(1)}s</p>
          <p>Baristas: {game.baristaCount}</p>
          <p>Customer Capacity: {game.customerCapacity}</p>
          <p>Barista Efficiency: {game.baristaEfficiency}</p>
        </div>
      </Modal>

      <Modal isOpen={activeModal === 'staff'} onClose={() => setActiveModal('main')} title="Staff Management">
        <Button onClick={() => game.upgradeBaristaCount()} cost={game.baristaCountCost} icon={Users}>
          Hire New Barista
        </Button>
        <Button onClick={() => game.upgradeBaristaEfficiency()} cost={game.baristaEfficiencyCost} icon={Coffee}>
          Improve Efficiency
        </Button>
      </Modal>

      <Modal isOpen={activeModal === 'product'} onClose={() => setActiveModal('main')} title="Product Management">
        <Button onClick={() => game.upgradeCoffeePrice()} cost={game.coffeePriceCost} icon={DollarSign}>
          Increase Coffee Price
        </Button>
        <Button onClick={() => game.upgradeCoffeeSpeed()} cost={game.coffeeSpeedCost} icon={Coffee}>
          Faster Coffee Making
        </Button>
      </Modal>

      <Modal isOpen={activeModal === 'customer'} onClose={() => setActiveModal('main')} title="Customer Service">
        <Button onClick={() => game.upgradeCustomerCapacity()} cost={game.customerCapacityCost} icon={Users}>
          Increase Customer Capacity
        </Button>
      </Modal>
    </div>
  );
};

export default GameUI;
