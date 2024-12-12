import React, { useState, useEffect } from 'react';

const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  return (
    <div className="modal-overlay" style={{
      position: 'absolute',
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
      <div className="modal-content" style={{
        backgroundColor: '#1a1a2e',
        border: '2px solid #7C45CB',
        borderRadius: '8px',
        padding: '20px',
        width: '80%',
        maxWidth: '600px',
        maxHeight: '80vh',
        overflow: 'auto',
        boxShadow: '0 0 20px rgba(124, 69, 203, 0.3)',
        position: 'relative'
      }}>
        <h2 style={{
          fontFamily: 'Orbitron',
          color: '#fff',
          marginBottom: '20px',
          borderBottom: '2px solid #7C45CB',
          paddingBottom: '10px'
        }}>{title}</h2>
        <button onClick={onClose} style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
          background: 'none',
          border: 'none',
          color: '#fff',
          fontSize: '20px',
          cursor: 'pointer'
        }}>×</button>
        {children}
      </div>
    </div>
  );
};

const Button = ({ onClick, children, cost, style }) => (
  <button onClick={onClick} style={{
    margin: '5px',
    padding: '10px 20px',
    fontSize: '14px',
    color: '#fff',
    border: '2px solid #7C45CB',
    borderRadius: '4px',
    cursor: 'pointer',
    backgroundColor: 'rgba(124, 69, 203, 0.2)',
    transition: 'all 0.3s ease',
    fontFamily: 'Roboto',
    ...style,
    ':hover': {
      backgroundColor: 'rgba(124, 69, 203, 0.4)',
      transform: 'translateY(-2px)'
    }
  }}>
    {children} {cost && `(${cost} points)`}
  </button>
);

const HUD = ({ game, onOpenMenu }) => (
  <div style={{
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    padding: '15px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    background: 'linear-gradient(180deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 100%)'
  }}>
    <div style={{ fontFamily: 'Press Start 2P', fontSize: '20px', color: '#fff' }}>
      {game.score}
    </div>
    <Button onClick={onOpenMenu} style={{ backgroundColor: 'rgba(124, 69, 203, 0.3)' }}>
      Menu
    </Button>
  </div>
);

const StatsPanel = ({ game }) => (
  <div style={{ color: '#fff', fontFamily: 'Roboto' }}>
    <div style={{ marginBottom: '20px' }}>
      <h3 style={{ fontFamily: 'Orbitron', color: '#7C45CB' }}>Paddle Stats</h3>
      <p>Size: {game.paddleSize}</p>
      <p>Speed: {game.paddleSpeed.toFixed(1)}</p>
    </div>
    <div style={{ marginBottom: '20px' }}>
      <h3 style={{ fontFamily: 'Orbitron', color: '#7C45CB' }}>Ball Stats</h3>
      <p>Speed: {game.ballSpeed.toFixed(1)}</p>
      <p>Count: {game.ballCount}</p>
    </div>
    <div>
      <h3 style={{ fontFamily: 'Orbitron', color: '#7C45CB' }}>Scoring</h3>
      <p>Multiplier: {game.pointsMultiplier}x</p>
    </div>
  </div>
);

const UpgradePanel = ({ game }) => (
  <div style={{ color: '#fff', fontFamily: 'Roboto' }}>
    <div style={{ marginBottom: '20px' }}>
      <h3 style={{ fontFamily: 'Orbitron', color: '#7C45CB' }}>Paddle Upgrades</h3>
      <Button onClick={() => game.upgradePaddleSize()} cost={game.paddleSizeCost}>
        Increase Size
      </Button>
      <Button onClick={() => game.upgradePaddleSpeed()} cost={game.paddleSpeedCost}>
        Increase Speed
      </Button>
    </div>
    <div style={{ marginBottom: '20px' }}>
      <h3 style={{ fontFamily: 'Orbitron', color: '#7C45CB' }}>Ball Upgrades</h3>
      <Button onClick={() => game.upgradeBallSpeed()} cost={game.ballSpeedCost}>
        Increase Speed
      </Button>
      <Button onClick={() => game.upgradeMultiBall()} cost={game.multiBallCost}>
        Add Ball
      </Button>
    </div>
    <div>
      <h3 style={{ fontFamily: 'Orbitron', color: '#7C45CB' }}>Score Upgrades</h3>
      <Button onClick={() => game.upgradePointsMultiplier()} cost={game.pointsMultiplierCost}>
        Increase Multiplier
      </Button>
    </div>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('stats');

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <HUD game={game} onOpenMenu={() => setMenuOpen(true)} />
      
      <Modal isOpen={menuOpen} onClose={() => setMenuOpen(false)} title="Game Menu">
        <div style={{ marginBottom: '20px' }}>
          <Button 
            onClick={() => setActiveTab('stats')} 
            style={{ backgroundColor: activeTab === 'stats' ? 'rgba(124, 69, 203, 0.4)' : undefined }}
          >
            Stats
          </Button>
          <Button 
            onClick={() => setActiveTab('upgrades')} 
            style={{ backgroundColor: activeTab === 'upgrades' ? 'rgba(124, 69, 203, 0.4)' : undefined }}
          >
            Upgrades
          </Button>
        </div>
        
        {activeTab === 'stats' && <StatsPanel game={game} />}
        {activeTab === 'upgrades' && <UpgradePanel game={game} />}
      </Modal>
    </div>
  );
};

export default GameUI;
