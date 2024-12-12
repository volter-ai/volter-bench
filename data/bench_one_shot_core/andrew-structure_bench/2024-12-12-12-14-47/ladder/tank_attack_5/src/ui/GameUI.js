import React, { useState, useEffect } from 'react';
import { Settings, X, Shield, Zap, Target, Plus, Crosshair, Gauge } from 'lucide-react';

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
      backdropFilter: 'blur(4px)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000,
    }}>
      <div style={{
        backgroundColor: 'rgba(16, 24, 39, 0.95)',
        border: '1px solid #2563eb',
        borderRadius: '8px',
        padding: '20px',
        width: '80%',
        maxWidth: '600px',
        maxHeight: '80vh',
        overflow: 'auto',
        boxShadow: '0 0 20px rgba(37, 99, 235, 0.2)',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
        }}>
          <h2 style={{
            margin: 0,
            fontFamily: 'Orbitron',
            color: '#2563eb',
            fontSize: '1.5rem',
          }}>{title}</h2>
          <X
            onClick={onClose}
            style={{ cursor: 'pointer', color: '#6b7280' }}
            size={20}
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
      backgroundColor: disabled ? '#1f2937' : '#1e40af',
      fontFamily: 'Orbitron',
      transition: 'all 0.2s',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      opacity: disabled ? 0.5 : 1,
    }}
  >
    {children} <span style={{ color: '#93c5fd' }}>({cost})</span>
  </button>
);

const StatBar = ({ label, value, maxValue }) => (
  <div style={{ marginBottom: '10px' }}>
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      marginBottom: '4px',
      fontFamily: 'Share Tech Mono',
      color: '#93c5fd',
    }}>
      <span>{label}</span>
      <span>{value.toFixed(1)}</span>
    </div>
    <div style={{
      width: '100%',
      height: '4px',
      backgroundColor: '#1f2937',
      borderRadius: '2px',
    }}>
      <div style={{
        width: `${(value / maxValue) * 100}%`,
        height: '100%',
        backgroundColor: '#2563eb',
        borderRadius: '2px',
        transition: 'width 0.3s',
      }} />
    </div>
  </div>
);

const HUD = ({ game }) => (
  <div style={{
    position: 'absolute',
    top: '20px',
    left: '20px',
    padding: '15px',
    backgroundColor: 'rgba(17, 24, 39, 0.8)',
    borderRadius: '8px',
    border: '1px solid #2563eb',
    color: '#e5e7eb',
    fontFamily: 'Orbitron',
    boxShadow: '0 0 10px rgba(37, 99, 235, 0.2)',
  }}>
    <div style={{ display: 'flex', gap: '20px' }}>
      <div>Credits: {game.credits}</div>
      <div>Tanks: {game.tankCount}</div>
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
    <div style={{ width: '100%', height: '100%' }}>
      <HUD game={game} />
      
      <div style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        display: 'flex',
        gap: '10px',
      }}>
        <button
          onClick={() => setShowStats(true)}
          style={{
            backgroundColor: 'rgba(17, 24, 39, 0.8)',
            border: '1px solid #2563eb',
            borderRadius: '8px',
            padding: '10px',
            cursor: 'pointer',
          }}
        >
          <Target color="#2563eb" size={24} />
        </button>
        <button
          onClick={() => setShowUpgrades(true)}
          style={{
            backgroundColor: 'rgba(17, 24, 39, 0.8)',
            border: '1px solid #2563eb',
            borderRadius: '8px',
            padding: '10px',
            cursor: 'pointer',
          }}
        >
          <Settings color="#2563eb" size={24} />
        </button>
      </div>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Tank Statistics">
        <div style={{ display: 'grid', gap: '15px' }}>
          <StatBar label="Speed" value={game.tankSpeed} maxValue={200} />
          <StatBar label="Health" value={game.tankHealth} maxValue={200} />
          <StatBar label="Damage" value={game.tankDamage} maxValue={50} />
          <StatBar label="Fire Rate" value={game.tankFireRate} maxValue={3} />
          <StatBar label="Range" value={game.tankRange} maxValue={400} />
        </div>
      </Modal>

      <Modal isOpen={showUpgrades} onClose={() => setShowUpgrades(false)} title="Command Center">
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '20px',
        }}>
          <div>
            <h3 style={{ color: '#93c5fd', fontFamily: 'Orbitron', marginBottom: '10px' }}>Offensive</h3>
            <Button onClick={() => game.upgradeTankDamage()} cost={game.costs.TANK_DAMAGE} disabled={game.credits < game.costs.TANK_DAMAGE}>
              <Crosshair size={16} /> Damage
            </Button>
            <Button onClick={() => game.upgradeFireRate()} cost={game.costs.TANK_FIRE_RATE} disabled={game.credits < game.costs.TANK_FIRE_RATE}>
              <Zap size={16} /> Fire Rate
            </Button>
          </div>
          
          <div>
            <h3 style={{ color: '#93c5fd', fontFamily: 'Orbitron', marginBottom: '10px' }}>Defensive</h3>
            <Button onClick={() => game.upgradeTankHealth()} cost={game.costs.TANK_HEALTH} disabled={game.credits < game.costs.TANK_HEALTH}>
              <Shield size={16} /> Health
            </Button>
            <Button onClick={() => game.upgradeRange()} cost={game.costs.TANK_RANGE} disabled={game.credits < game.costs.TANK_RANGE}>
              <Target size={16} /> Range
            </Button>
          </div>
          
          <div>
            <h3 style={{ color: '#93c5fd', fontFamily: 'Orbitron', marginBottom: '10px' }}>Tactical</h3>
            <Button onClick={() => game.upgradeTankSpeed()} cost={game.costs.TANK_SPEED} disabled={game.credits < game.costs.TANK_SPEED}>
              <Gauge size={16} /> Speed
            </Button>
            <Button onClick={() => game.upgradeTankCount()} cost={game.costs.TANK_COUNT} disabled={game.credits < game.costs.TANK_COUNT}>
              <Plus size={16} /> New Tank
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default GameUI;
