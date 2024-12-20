import React, { useState, useEffect } from 'react';
import { Settings, X, Activity, ChevronRight, Award, Circle, Square } from 'lucide-react';

const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  
  return (
    <div className="modal-backdrop" 
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0,0,0,0.85)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000,
      }}>
      <div className="modal-content" 
        style={{
          backgroundColor: '#1a1f2e',
          border: '2px solid #7C45CB',
          borderRadius: '8px',
          padding: '20px',
          width: '80%',
          maxWidth: '500px',
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
          borderBottom: '2px solid #7C45CB',
          paddingBottom: '10px'
        }}>
          <h2 style={{ margin: 0, color: '#00FFFF', fontFamily: 'Orbitron' }}>{title}</h2>
          <X 
            onClick={onClose}
            style={{ cursor: 'pointer', color: '#00FFFF' }}
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
      padding: '10px 20px',
      fontSize: '14px',
      color: disabled ? '#666' : '#00FFFF',
      border: '2px solid',
      borderColor: disabled ? '#444' : '#7C45CB',
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: '#1a1f2e',
      borderRadius: '4px',
      fontFamily: 'Orbitron',
      transition: 'all 0.3s ease',
      boxShadow: disabled ? 'none' : '0 0 10px rgba(124, 69, 203, 0.3)',
      ':hover': {
        boxShadow: disabled ? 'none' : '0 0 15px rgba(124, 69, 203, 0.5)',
      }
    }}>
    {children} {cost && `(${cost} points)`}
  </button>
);

const HUD = ({ game }) => (
  <div style={{ 
    position: 'absolute', 
    top: '10px', 
    left: '50%', 
    transform: 'translateX(-50%)',
    padding: '10px 20px',
    backgroundColor: 'rgba(26, 31, 46, 0.9)',
    color: '#00FFFF',
    borderRadius: '20px',
    border: '2px solid #7C45CB',
    fontFamily: 'Orbitron',
    boxShadow: '0 0 15px rgba(124, 69, 203, 0.3)',
  }}>
    <p style={{ margin: 0 }}>Score: {game.score}</p>
  </div>
);

const MenuButton = ({ icon: Icon, onClick, style }) => (
  <div
    onClick={onClick}
    style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: '40px',
      height: '40px',
      backgroundColor: '#1a1f2e',
      border: '2px solid #7C45CB',
      borderRadius: '50%',
      cursor: 'pointer',
      boxShadow: '0 0 10px rgba(124, 69, 203, 0.3)',
      ...style
    }}
  >
    <Icon size={24} color="#00FFFF" />
  </div>
);

const UpgradeSection = ({ title, children }) => (
  <div style={{
    marginBottom: '20px',
    padding: '15px',
    backgroundColor: 'rgba(124, 69, 203, 0.1)',
    borderRadius: '8px',
    border: '1px solid #7C45CB',
  }}>
    <h3 style={{ 
      color: '#00FFFF', 
      marginTop: 0,
      marginBottom: '10px',
      fontFamily: 'Orbitron'
    }}>{title}</h3>
    {children}
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [showMainMenu, setShowMainMenu] = useState(false);
  const [showUpgrades, setShowUpgrades] = useState(false);
  const [showStats, setShowStats] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%', color: '#d3d3d3' }}>
      <HUD game={game} />
      
      <MenuButton 
        icon={Activity}
        onClick={() => setShowMainMenu(true)}
        style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
        }}
      />

      <Modal isOpen={showMainMenu} onClose={() => setShowMainMenu(false)} title="Main Menu">
        <Button onClick={() => setShowStats(true)}>Statistics <ChevronRight size={16} /></Button>
        <Button onClick={() => setShowUpgrades(true)}>Upgrades <ChevronRight size={16} /></Button>
      </Modal>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Statistics">
        <div style={{ color: '#00FFFF', fontFamily: 'Orbitron' }}>
          <p>Balls: {game.ballCount}</p>
          <p>Ball Speed: {game.ballSpeed.toFixed(0)}</p>
          <p>Paddle Size: {game.paddleSize.toFixed(0)}</p>
          <p>Paddle Speed: {game.paddleSpeed.toFixed(0)}</p>
          <p>Points per Hit: {game.pointsPerHit}</p>
        </div>
      </Modal>

      <Modal isOpen={showUpgrades} onClose={() => setShowUpgrades(false)} title="Upgrades">
        <UpgradeSection title="Ball Upgrades">
          <Button onClick={() => game.upgradeBallSpeed()} cost={game.ballSpeedCost} disabled={game.score < game.ballSpeedCost}>
            Upgrade Ball Speed
          </Button>
          <Button onClick={() => game.addBall()} cost={game.ballCountCost} disabled={game.score < game.ballCountCost}>
            Add Ball
          </Button>
        </UpgradeSection>

        <UpgradeSection title="Paddle Upgrades">
          <Button onClick={() => game.upgradePaddleSize()} cost={game.paddleSizeCost} disabled={game.score < game.paddleSizeCost}>
            Upgrade Paddle Size
          </Button>
          <Button onClick={() => game.upgradePaddleSpeed()} cost={game.paddleSpeedCost} disabled={game.score < game.paddleSpeedCost}>
            Upgrade Paddle Speed
          </Button>
        </UpgradeSection>

        <UpgradeSection title="Point Upgrades">
          <Button onClick={() => game.upgradePointsPerHit()} cost={game.pointsPerHitCost} disabled={game.score < game.pointsPerHitCost}>
            Upgrade Points Per Hit
          </Button>
        </UpgradeSection>
      </Modal>
    </div>
  );
};

export default GameUI;
