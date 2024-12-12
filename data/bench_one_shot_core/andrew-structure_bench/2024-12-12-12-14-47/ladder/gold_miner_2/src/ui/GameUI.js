import React, { useState, useEffect } from 'react';
import { Settings, Users, Database, X, BarChart2 } from 'lucide-react';

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
      zIndex: 1000,
    }} onClick={onClose}>
      <div style={{
        backgroundColor: '#1a1a2e',
        padding: '20px',
        borderRadius: '10px',
        border: '2px solid #4a9eff',
        boxShadow: '0 0 20px rgba(74, 158, 255, 0.2)',
        maxWidth: '80%',
        maxHeight: '80%',
        overflow: 'auto',
        position: 'relative',
      }} onClick={e => e.stopPropagation()}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
          borderBottom: '2px solid #4a9eff',
          paddingBottom: '10px',
        }}>
          <h2 style={{
            margin: 0,
            fontFamily: 'Orbitron',
            color: '#4a9eff',
          }}>{title}</h2>
          <X
            onClick={onClose}
            style={{ cursor: 'pointer', color: '#4a9eff' }}
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
      color: disabled ? '#666' : '#fff',
      border: 'none',
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: disabled ? '#2a2a3e' : '#4a9eff',
      borderRadius: '5px',
      fontFamily: 'Roboto',
      transition: 'all 0.2s',
      opacity: disabled ? 0.7 : 1,
    }}>
    {children} ({cost} gold)
  </button>
);

const IconButton = ({ Icon, onClick, tooltip }) => (
  <div style={{
    position: 'relative',
    margin: '0 5px',
  }}>
    <div style={{
      padding: '8px',
      backgroundColor: '#1a1a2e',
      borderRadius: '5px',
      cursor: 'pointer',
      border: '1px solid #4a9eff',
      transition: 'all 0.2s',
    }} onClick={onClick}>
      <Icon size={20} color="#4a9eff" />
    </div>
    <div style={{
      position: 'absolute',
      bottom: '-25px',
      left: '50%',
      transform: 'translateX(-50%)',
      backgroundColor: '#1a1a2e',
      padding: '3px 8px',
      borderRadius: '3px',
      fontSize: '12px',
      opacity: 0,
      transition: 'opacity 0.2s',
      pointerEvents: 'none',
      whiteSpace: 'nowrap',
    }}>
      {tooltip}
    </div>
  </div>
);

const HUD = ({ game, onOpenStats, onOpenUpgrades }) => (
  <div style={{
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    padding: '10px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: 'rgba(26, 26, 46, 0.9)',
    borderBottom: '2px solid #4a9eff',
  }}>
    <div style={{
      fontFamily: 'Orbitron',
      color: '#4a9eff',
      fontSize: '18px',
    }}>
      Gold: {Math.floor(game.gold)}
    </div>
    <div style={{
      display: 'flex',
      alignItems: 'center',
    }}>
      <IconButton Icon={BarChart2} onClick={onOpenStats} tooltip="Statistics" />
      <IconButton Icon={Database} onClick={onOpenUpgrades} tooltip="Upgrades" />
    </div>
  </div>
);

const StatsModal = ({ game, isOpen, onClose }) => (
  <Modal isOpen={isOpen} onClose={onClose} title="Statistics">
    <div style={{ color: '#fff', fontFamily: 'Roboto' }}>
      <p>Miners: {game.minerCount}</p>
      <p>Mining Speed: {game.miningSpeed.toFixed(1)}</p>
      <p>Carrying Capacity: {game.carryingCapacity}</p>
      <p>Maximum Mines: {game.maxMines}</p>
      <p>Mine Size: {game.mineSize}</p>
    </div>
  </Modal>
);

const UpgradesModal = ({ game, isOpen, onClose }) => (
  <Modal isOpen={isOpen} onClose={onClose} title="Upgrades">
    <div style={{ color: '#fff', fontFamily: 'Roboto' }}>
      <h3 style={{ color: '#4a9eff', fontFamily: 'Orbitron' }}>Miner Management</h3>
      <Button onClick={() => game.upgradeMinerCount()} cost={game.minerCost} disabled={game.gold < game.minerCost}>
        Add Miner
      </Button>
      <Button onClick={() => game.upgradeMiningSpeed()} cost={game.speedCost} disabled={game.gold < game.speedCost}>
        Upgrade Speed
      </Button>

      <h3 style={{ color: '#4a9eff', fontFamily: 'Orbitron', marginTop: '20px' }}>Mining Operations</h3>
      <Button onClick={() => game.upgradeCarryingCapacity()} cost={game.capacityCost} disabled={game.gold < game.capacityCost}>
        Upgrade Capacity
      </Button>
      <Button onClick={() => game.upgradeMineSize()} cost={game.mineSizeCost} disabled={game.gold < game.mineSizeCost}>
        Increase Mine Size
      </Button>

      <h3 style={{ color: '#4a9eff', fontFamily: 'Orbitron', marginTop: '20px' }}>Infrastructure</h3>
      <Button onClick={() => game.upgradeMaxMines()} cost={game.maxMinesCost} disabled={game.gold < game.maxMinesCost}>
        Add Max Mine
      </Button>
    </div>
  </Modal>
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
