import React, { useState, useEffect } from 'react';
import { Shield, Zap, Target, X, BarChart2, ChevronUp } from 'lucide-react';

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
        backgroundColor: '#1a2634',
        border: '2px solid #30465c',
        borderRadius: '8px',
        padding: '20px',
        minWidth: '300px',
        position: 'relative',
        boxShadow: '0 0 20px rgba(0,149,255,0.15)'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '15px'
        }}>
          <h2 style={{
            margin: 0,
            fontFamily: 'Orbitron',
            color: '#00ff88',
            fontSize: '18px'
          }}>{title}</h2>
          <X
            onClick={onClose}
            style={{
              cursor: 'pointer',
              color: '#6c8aa3'
            }}
          />
        </div>
        {children}
      </div>
    </div>
  );
};

const Button = ({ onClick, children, cost, game, disabled }) => {
  const canAfford = game.credits >= cost;
  
  return (
    <button
      onClick={onClick}
      disabled={disabled || !canAfford}
      style={{
        margin: '5px',
        padding: '8px 15px',
        fontSize: '14px',
        color: canAfford ? '#d3d3d3' : '#666',
        border: 'none',
        cursor: canAfford ? 'pointer' : 'not-allowed',
        backgroundColor: canAfford ? '#1c3854' : '#1a2634',
        borderRadius: '4px',
        fontFamily: 'Roboto',
        transition: 'all 0.2s',
        position: 'relative',
        boxShadow: canAfford ? '0 0 10px rgba(0,149,255,0.15)' : 'none',
        ':hover': {
          backgroundColor: '#264666'
        }
      }}>
      {children}
      <div style={{
        fontSize: '12px',
        color: canAfford ? '#00ff88' : '#666'
      }}>
        {cost} credits
      </div>
    </button>
  );
};

const HUD = ({ game, onOpenStats, onOpenUpgrades }) => (
  <div style={{
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    padding: '15px',
    background: 'linear-gradient(180deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 100%)',
    color: '#d3d3d3',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontFamily: 'Orbitron'
  }}>
    <div style={{ display: 'flex', gap: '20px' }}>
      <div style={{ color: '#00ff88' }}>Credits: {game.credits}</div>
      <div>Tanks: {game.tankCount}</div>
    </div>
    <div style={{ display: 'flex', gap: '10px' }}>
      <button
        onClick={onOpenStats}
        style={{
          backgroundColor: 'transparent',
          border: '1px solid #30465c',
          borderRadius: '4px',
          padding: '5px 10px',
          color: '#6c8aa3',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '5px'
        }}
      >
        <BarChart2 size={16} /> Stats
      </button>
      <button
        onClick={onOpenUpgrades}
        style={{
          backgroundColor: '#1c3854',
          border: 'none',
          borderRadius: '4px',
          padding: '5px 10px',
          color: '#00ff88',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '5px'
        }}
      >
        <ChevronUp size={16} /> Upgrades
      </button>
    </div>
  </div>
);

const StatsModal = ({ isOpen, onClose, game }) => (
  <Modal isOpen={isOpen} onClose={onClose} title="Tank Statistics">
    <div style={{
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '15px',
      color: '#d3d3d3',
      fontFamily: 'Roboto'
    }}>
      <div>Damage: {Math.floor(game.tankDamage)}</div>
      <div>Health: {Math.floor(game.tankHealth)}</div>
      <div>Fire Rate: {game.fireRate.toFixed(1)}/s</div>
      <div>Range: {Math.floor(game.detectionRange)}</div>
      <div>Speed: {Math.floor(game.tankSpeed)}</div>
      <div>Tank Count: {game.tankCount}</div>
    </div>
  </Modal>
);

const UpgradeModal = ({ isOpen, onClose, game }) => {
  const [category, setCategory] = useState(null);
  
  const categories = {
    offensive: {
      icon: <Zap />,
      title: "Offensive",
      upgrades: [
        { name: "Damage", action: () => game.upgradeTankDamage(), cost: game.costs.TANK_DAMAGE },
        { name: "Fire Rate", action: () => game.upgradeFireRate(), cost: game.costs.FIRE_RATE }
      ]
    },
    defensive: {
      icon: <Shield />,
      title: "Defensive",
      upgrades: [
        { name: "Health", action: () => game.upgradeTankHealth(), cost: game.costs.TANK_HEALTH },
        { name: "Range", action: () => game.upgradeDetectionRange(), cost: game.costs.DETECTION_RANGE }
      ]
    },
    tactical: {
      icon: <Target />,
      title: "Tactical",
      upgrades: [
        { name: "Add Tank", action: () => game.upgradeTankCount(), cost: game.costs.TANK_COUNT },
        { name: "Speed", action: () => game.upgradeTankSpeed(), cost: game.costs.TANK_SPEED }
      ]
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Upgrades">
      {!category ? (
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr 1fr',
          gap: '10px'
        }}>
          {Object.entries(categories).map(([key, cat]) => (
            <button
              key={key}
              onClick={() => setCategory(key)}
              style={{
                padding: '15px',
                backgroundColor: '#1c3854',
                border: 'none',
                borderRadius: '4px',
                color: '#00ff88',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '10px'
              }}
            >
              {cat.icon}
              {cat.title}
            </button>
          ))}
        </div>
      ) : (
        <div>
          <button
            onClick={() => setCategory(null)}
            style={{
              backgroundColor: 'transparent',
              border: 'none',
              color: '#6c8aa3',
              cursor: 'pointer',
              marginBottom: '15px'
            }}
          >
            ← Back
          </button>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '10px'
          }}>
            {categories[category].upgrades.map((upgrade, index) => (
              <Button
                key={index}
                onClick={upgrade.action}
                cost={upgrade.cost}
                game={game}
              >
                {upgrade.name}
              </Button>
            ))}
          </div>
        </div>
      )}
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
    <div style={{ width: '100%', height: '100%', color: '#d3d3d3' }}>
      <HUD
        game={game}
        onOpenStats={() => setShowStats(true)}
        onOpenUpgrades={() => setShowUpgrades(true)}
      />
      <StatsModal
        isOpen={showStats}
        onClose={() => setShowStats(false)}
        game={game}
      />
      <UpgradeModal
        isOpen={showUpgrades}
        onClose={() => setShowUpgrades(false)}
        game={game}
      />
    </div>
  );
};

export default GameUI;
