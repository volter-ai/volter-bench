import React, { useState, useEffect } from 'react';
import { Settings, Activity, Shield, Zap, Users, DollarSign, X, ChevronRight } from 'lucide-react';

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
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: 'rgba(44, 62, 80, 0.95)',
        border: '2px solid #7C45CB',
        borderRadius: '8px',
        padding: '20px',
        minWidth: '400px',
        position: 'relative'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px'
        }}>
          <h2 style={{
            margin: 0,
            fontFamily: 'Orbitron',
            color: '#fff',
            fontSize: '1.5em'
          }}>{title}</h2>
          <X
            onClick={onClose}
            style={{ cursor: 'pointer', color: '#fff' }}
          />
        </div>
        {children}
      </div>
    </div>
  );
};

const Button = ({ onClick, children, cost, icon: Icon }) => (
  <button
    onClick={onClick}
    style={{
      margin: '5px',
      padding: '10px 15px',
      fontSize: '14px',
      color: '#fff',
      border: '2px solid #7C45CB',
      borderRadius: '4px',
      cursor: 'pointer',
      backgroundColor: 'rgba(124, 69, 203, 0.2)',
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      transition: 'all 0.2s',
      fontFamily: 'Roboto',
      width: '100%',
      justifyContent: 'space-between'
    }}
    onMouseEnter={e => e.target.style.backgroundColor = 'rgba(124, 69, 203, 0.4)'}
    onMouseLeave={e => e.target.style.backgroundColor = 'rgba(124, 69, 203, 0.2)'}
  >
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      {Icon && <Icon size={16} />}
      {children}
    </div>
    <div style={{ opacity: 0.8 }}>{cost} credits</div>
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
    fontFamily: 'Orbitron'
  }}>
    <div style={{ display: 'flex', gap: '20px' }}>
      <span><DollarSign size={16} style={{ verticalAlign: 'middle' }} /> {Math.floor(game.credits)}</span>
      <span><Users size={16} style={{ verticalAlign: 'middle' }} /> {game.tankCount}</span>
    </div>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [showStats, setShowStats] = useState(false);
  const [showUpgrades, setShowUpgrades] = useState(false);
  const [upgradeCategory, setUpgradeCategory] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;

  const renderUpgradeCategory = () => {
    switch (upgradeCategory) {
      case 'combat':
        return (
          <>
            <Button icon={Shield} onClick={() => game.upgradeTankHealth()} cost={game.tankHealthCost}>
              Upgrade Tank Health
            </Button>
            <Button icon={Zap} onClick={() => game.upgradeTankDamage()} cost={game.tankDamageCost}>
              Upgrade Tank Damage
            </Button>
          </>
        );
      case 'mobility':
        return (
          <>
            <Button icon={Activity} onClick={() => game.upgradeTankSpeed()} cost={game.tankSpeedCost}>
              Upgrade Tank Speed
            </Button>
            <Button icon={Users} onClick={() => game.upgradeTankCount()} cost={game.tankCountCost}>
              Increase Tank Count
            </Button>
          </>
        );
      case 'economy':
        return (
          <Button icon={DollarSign} onClick={() => game.upgradeBaseReward()} cost={game.baseRewardCost}>
            Increase Base Reward
          </Button>
        );
      default:
        return (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <Button icon={ChevronRight} onClick={() => setUpgradeCategory('combat')} cost="View">
              Combat Upgrades
            </Button>
            <Button icon={ChevronRight} onClick={() => setUpgradeCategory('mobility')} cost="View">
              Mobility Upgrades
            </Button>
            <Button icon={ChevronRight} onClick={() => setUpgradeCategory('economy')} cost="View">
              Economy Upgrades
            </Button>
          </div>
        );
    }
  };

  return (
    <div style={{ width: '100%', height: '100%', color: '#fff', fontFamily: 'Roboto' }}>
      <HUD game={game} />
      
      <div style={{ position: 'absolute', bottom: '10px', right: '10px', display: 'flex', gap: '10px' }}>
        <Activity
          onClick={() => setShowStats(true)}
          style={{ cursor: 'pointer', padding: '8px', backgroundColor: 'rgba(0,0,0,0.5)', borderRadius: '4px' }}
        />
        <Settings
          onClick={() => setShowUpgrades(true)}
          style={{ cursor: 'pointer', padding: '8px', backgroundColor: 'rgba(0,0,0,0.5)', borderRadius: '4px' }}
        />
      </div>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Tank Statistics">
        <div style={{ display: 'grid', gap: '10px' }}>
          <div>Tank Health: {Math.floor(game.tankHealth)}</div>
          <div>Tank Damage: {Math.floor(game.tankDamage)}</div>
          <div>Tank Speed: {Math.floor(game.tankSpeed)}</div>
          <div>Base Reward: {Math.floor(game.baseReward)}</div>
        </div>
      </Modal>

      <Modal
        isOpen={showUpgrades}
        onClose={() => {
          setShowUpgrades(false);
          setUpgradeCategory(null);
        }}
        title={upgradeCategory ? `${upgradeCategory.charAt(0).toUpperCase() + upgradeCategory.slice(1)} Upgrades` : "Upgrades"}
      >
        {renderUpgradeCategory()}
        {upgradeCategory && (
          <Button
            onClick={() => setUpgradeCategory(null)}
            cost="Back"
            style={{ marginTop: '20px' }}
          >
            Back to Categories
          </Button>
        )}
      </Modal>
    </div>
  );
};

export default GameUI;
