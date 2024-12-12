import React, { useState, useEffect } from 'react';
import { Activity, Award, Box, ChevronRight, X } from 'lucide-react';

const Modal = ({ isOpen, onClose, children, title }) => {
  if (!isOpen) return null;
  return (
    <div className="modal-backdrop" onClick={onClose} style={{
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.8)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 100,
    }}>
      <div className="modal-content" onClick={e => e.stopPropagation()} style={{
        backgroundColor: '#1a1a2e',
        border: '2px solid #7C45CB',
        borderRadius: '10px',
        padding: '20px',
        width: '80%',
        maxWidth: '600px',
        maxHeight: '80%',
        overflow: 'auto',
        boxShadow: '0 0 20px rgba(124, 69, 203, 0.3)',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ margin: 0, fontFamily: 'Orbitron', color: '#7C45CB' }}>{title}</h2>
          <X onClick={onClose} style={{ cursor: 'pointer', color: '#7C45CB' }} />
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
      color: disabled ? '#666' : '#fff',
      border: 'none',
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: disabled ? '#333' : '#7C45CB',
      borderRadius: '5px',
      fontFamily: 'Orbitron',
      transition: 'all 0.2s',
      opacity: disabled ? 0.5 : 1,
    }}
  >
    {children} {cost && `(${cost} points)`}
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
    fontFamily: 'Orbitron',
  }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span style={{ fontSize: '24px' }}>Score: {Math.floor(game.score)}</span>
      <span style={{ color: '#7C45CB' }}>Combo: x{game.consecutiveHits}</span>
    </div>
  </div>
);

const UpgradeSection = ({ title, upgrades }) => (
  <div style={{ marginBottom: '20px' }}>
    <h3 style={{ color: '#7C45CB', fontFamily: 'Orbitron', borderBottom: '1px solid #7C45CB' }}>{title}</h3>
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
      {upgrades}
    </div>
  </div>
);

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
    <div style={{ width: '100%', height: '100%', color: '#fff' }}>
      <HUD game={game} />
      
      <div style={{ position: 'absolute', bottom: '20px', right: '20px', display: 'flex', gap: '10px' }}>
        <Button onClick={() => setShowStats(true)}>
          <Activity size={20} />
        </Button>
        <Button onClick={() => setShowUpgrades(true)}>
          <Award size={20} />
        </Button>
      </div>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Statistics">
        <div style={{ fontFamily: 'Orbitron' }}>
          <p>Current Multiplier: x{(game.pointMultiplier * Math.pow(game.comboMultiplier, game.consecutiveHits - 1)).toFixed(2)}</p>
          <p>Paddle Height: {game.paddleHeight}</p>
          <p>Paddle Speed: {game.paddleSpeed.toFixed(1)}</p>
          <p>Ball Speed: {game.ballSpeed.toFixed(1)}</p>
          <p>Prediction Accuracy: {(game.paddlePrediction * 100).toFixed(1)}%</p>
        </div>
      </Modal>

      <Modal isOpen={showUpgrades} onClose={() => setShowUpgrades(false)} title="Upgrades">
        <UpgradeSection title="Paddle Upgrades" upgrades={[
          <Button 
            onClick={() => game.upgradePaddleHeight()} 
            cost={game.paddleHeightCost}
            disabled={game.score < game.paddleHeightCost}
          >
            Paddle Height
          </Button>,
          <Button 
            onClick={() => game.upgradePaddleSpeed()} 
            cost={game.paddleSpeedCost}
            disabled={game.score < game.paddleSpeedCost}
          >
            Paddle Speed
          </Button>,
          <Button 
            onClick={() => game.upgradePaddlePrediction()} 
            cost={game.paddlePredictionCost}
            disabled={game.score < game.paddlePredictionCost}
          >
            Prediction
          </Button>
        ]} />

        <UpgradeSection title="Ball Upgrades" upgrades={[
          <Button 
            onClick={() => game.upgradeBallSpeed()} 
            cost={game.ballSpeedCost}
            disabled={game.score < game.ballSpeedCost}
          >
            Ball Speed
          </Button>
        ]} />

        <UpgradeSection title="Scoring Upgrades" upgrades={[
          <Button 
            onClick={() => game.upgradePointMultiplier()} 
            cost={game.pointMultiplierCost}
            disabled={game.score < game.pointMultiplierCost}
          >
            Point Multiplier
          </Button>,
          <Button 
            onClick={() => game.upgradeComboMultiplier()} 
            cost={game.comboMultiplierCost}
            disabled={game.score < game.comboMultiplierCost}
          >
            Combo Multiplier
          </Button>
        ]} />
      </Modal>
    </div>
  );
};

export default GameUI;
