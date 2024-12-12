import React, { useState, useEffect } from 'react';
import { Settings, Activity, ArrowUpCircle, X, BarChart2 } from 'lucide-react';

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
      backdropFilter: 'blur(4px)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000
    }}>
      <div className="modal-content" style={{
        backgroundColor: 'rgba(16, 24, 39, 0.95)',
        border: '1px solid #2563eb',
        borderRadius: '8px',
        padding: '20px',
        width: '80%',
        maxWidth: '600px',
        maxHeight: '80vh',
        overflow: 'auto',
        boxShadow: '0 0 20px rgba(37, 99, 235, 0.2)',
        position: 'relative'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
          borderBottom: '1px solid rgba(37, 99, 235, 0.3)',
          paddingBottom: '10px'
        }}>
          <h2 style={{
            margin: 0,
            fontFamily: 'Orbitron',
            color: '#60a5fa',
            fontSize: '1.5rem'
          }}>{title}</h2>
          <X
            onClick={onClose}
            style={{
              cursor: 'pointer',
              color: '#60a5fa',
              transition: 'color 0.2s',
            }}
            onMouseOver={(e) => e.currentTarget.style.color = '#93c5fd'}
            onMouseOut={(e) => e.currentTarget.style.color = '#60a5fa'}
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
      border: '1px solid',
      borderColor: disabled ? '#374151' : '#2563eb',
      borderRadius: '4px',
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: disabled ? '#1f2937' : 'rgba(37, 99, 235, 0.2)',
      fontFamily: 'Rajdhani',
      transition: 'all 0.2s',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      width: '100%'
    }}
  >
    <span>{children}</span>
    <span style={{ fontSize: '12px', opacity: 0.8 }}>Cost: {cost} points</span>
  </button>
);

const HUD = ({ game }) => (
  <div style={{
    position: 'absolute',
    top: '20px',
    right: '20px',
    padding: '15px',
    backgroundColor: 'rgba(17, 24, 39, 0.8)',
    borderRadius: '8px',
    border: '1px solid #2563eb',
    color: '#60a5fa',
    fontFamily: 'Share Tech Mono',
    fontSize: '1.1rem',
    backdropFilter: 'blur(4px)'
  }}>
    <div>SCORE: {game.score}</div>
    <div>SPEED: {Math.floor(game.currentBallSpeed)}</div>
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
    <div style={{ width: '100%', height: '100%', color: '#e5e7eb' }}>
      <HUD game={game} />
      
      <div style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        display: 'flex',
        gap: '10px'
      }}>
        <BarChart2
          onClick={() => setShowStats(true)}
          style={{
            cursor: 'pointer',
            color: '#60a5fa',
            width: '28px',
            height: '28px'
          }}
        />
        <ArrowUpCircle
          onClick={() => setShowUpgrades(true)}
          style={{
            cursor: 'pointer',
            color: '#60a5fa',
            width: '28px',
            height: '28px'
          }}
        />
      </div>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Game Statistics">
        <div style={{ display: 'grid', gap: '15px', fontFamily: 'Rajdhani' }}>
          <div>Point Multiplier: {game.pointMultiplier}x</div>
          <div>Paddle Height: {game.paddleHeight}</div>
          <div>Paddle Speed: {game.paddleSpeed}</div>
          <div>Speed Scaling: {game.speedScaling.toFixed(2)}x</div>
          <div>Base Ball Speed: {game.ballSpeed}</div>
        </div>
      </Modal>

      <Modal isOpen={showUpgrades} onClose={() => setShowUpgrades(false)} title="Upgrades">
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '15px',
          padding: '10px'
        }}>
          <Button
            onClick={() => game.upgradePaddleHeight()}
            cost={game.paddleHeightCost}
            disabled={game.score < game.paddleHeightCost}
          >
            Paddle Height
          </Button>
          <Button
            onClick={() => game.upgradePaddleSpeed()}
            cost={game.paddleSpeedCost}
            disabled={game.score < game.paddleSpeedCost}
          >
            Paddle Speed
          </Button>
          <Button
            onClick={() => game.upgradePointMultiplier()}
            cost={game.pointMultiplierCost}
            disabled={game.score < game.pointMultiplierCost}
          >
            Point Multiplier
          </Button>
          <Button
            onClick={() => game.upgradeBallSpeed()}
            cost={game.ballSpeedCost}
            disabled={game.score < game.ballSpeedCost}
          >
            Ball Speed
          </Button>
          <Button
            onClick={() => game.upgradeSpeedScaling()}
            cost={game.speedScalingCost}
            disabled={game.score < game.speedScalingCost}
          >
            Speed Scaling
          </Button>
        </div>
      </Modal>
    </div>
  );
};

export default GameUI;
