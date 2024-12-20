import React, { useState, useEffect } from 'react';
import { Settings, X, User, Coins, Layout } from 'lucide-react';

const Modal = ({ isOpen, onClose, children, title }) => {
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
      zIndex: 1000,
    }}>
      <div style={{
        backgroundColor: '#1a1a2e',
        padding: '20px',
        borderRadius: '10px',
        border: '1px solid #7C45CB',
        boxShadow: '0 0 20px rgba(124, 69, 203, 0.3)',
        width: '80%',
        maxWidth: '600px',
        maxHeight: '80vh',
        overflow: 'auto',
        position: 'relative'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
          borderBottom: '1px solid #7C45CB',
          paddingBottom: '10px'
        }}>
          <h2 style={{ 
            margin: 0, 
            fontFamily: 'Orbitron',
            color: '#00FFFF',
            textShadow: '0 0 10px rgba(0, 255, 255, 0.5)'
          }}>{title}</h2>
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
      border: `1px solid ${disabled ? '#666' : '#7C45CB'}`,
      cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: '#1a1a2e',
      borderRadius: '5px',
      fontFamily: 'Roboto',
      transition: 'all 0.3s ease',
      boxShadow: disabled ? 'none' : '0 0 10px rgba(124, 69, 203, 0.3)',
      ':hover': {
        boxShadow: disabled ? 'none' : '0 0 15px rgba(124, 69, 203, 0.5)',
      }
    }}>
    {children} ({cost} coins)
  </button>
);

const HUD = ({ game }) => (
  <div style={{ 
    position: 'absolute', 
    top: '10px', 
    left: '10px', 
    padding: '10px 20px',
    backgroundColor: 'rgba(26, 26, 46, 0.9)',
    borderRadius: '20px',
    border: '1px solid #7C45CB',
    boxShadow: '0 0 10px rgba(124, 69, 203, 0.3)',
    color: '#00FFFF',
    fontFamily: 'Orbitron',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      <Coins size={20} />
      <span>{Math.floor(game.coins)}</span>
    </div>
  </div>
);

const TabButton = ({ active, onClick, children }) => (
  <button
    onClick={onClick}
    style={{
      padding: '10px 20px',
      backgroundColor: active ? '#7C45CB' : 'transparent',
      border: 'none',
      color: '#00FFFF',
      cursor: 'pointer',
      fontFamily: 'Orbitron',
      borderBottom: active ? '2px solid #00FFFF' : 'none',
    }}
  >
    {children}
  </button>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('stats');
  
  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;

  const renderStats = () => (
    <div style={{ color: '#d3d3d3', fontFamily: 'Roboto' }}>
      <p>Runners: {game.runnerCount}</p>
      <p>Tracks: {game.trackCount}</p>
      <p>Runner Speed: {game.runnerSpeed.toFixed(1)}</p>
      <p>Coin Value: {game.coinValue.toFixed(1)}</p>
      <p>Spawn Rate: {game.coinSpawnRate.toFixed(1)}/s</p>
    </div>
  );

  const renderUpgrades = () => (
    <div>
      <h3 style={{ color: '#00FFFF', fontFamily: 'Orbitron' }}>Runner Upgrades</h3>
      <Button 
        onClick={() => game.upgradeRunnerSpeed()} 
        cost={game.runnerSpeedCost}
        disabled={game.coins < game.runnerSpeedCost}
      >
        Upgrade Runner Speed
      </Button>
      <Button 
        onClick={() => game.upgradeRunnerCount()} 
        cost={game.runnerCountCost}
        disabled={game.coins < game.runnerCountCost}
      >
        Add Runner
      </Button>

      <h3 style={{ color: '#00FFFF', fontFamily: 'Orbitron', marginTop: '20px' }}>Coin Upgrades</h3>
      <Button 
        onClick={() => game.upgradeCoinValue()} 
        cost={game.coinValueCost}
        disabled={game.coins < game.coinValueCost}
      >
        Upgrade Coin Value
      </Button>
      <Button 
        onClick={() => game.upgradeCoinSpawnRate()} 
        cost={game.coinSpawnRateCost}
        disabled={game.coins < game.coinSpawnRateCost}
      >
        Upgrade Spawn Rate
      </Button>

      <h3 style={{ color: '#00FFFF', fontFamily: 'Orbitron', marginTop: '20px' }}>Track Upgrades</h3>
      <Button 
        onClick={() => game.upgradeTrackCount()} 
        cost={game.trackCountCost}
        disabled={game.coins < game.trackCountCost || game.trackCount >= game.MAX_TRACKS}
      >
        Add Track
      </Button>
    </div>
  );

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <HUD game={game} />
      
      <Settings
        onClick={() => setIsMenuOpen(true)}
        style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
          width: '24px',
          height: '24px',
          cursor: 'pointer',
          color: '#00FFFF'
        }}
      />

      <Modal 
        isOpen={isMenuOpen} 
        onClose={() => setIsMenuOpen(false)}
        title="Game Menu"
      >
        <div>
          <div style={{ borderBottom: '1px solid #7C45CB', marginBottom: '20px' }}>
            <TabButton 
              active={activeTab === 'stats'} 
              onClick={() => setActiveTab('stats')}
            >
              Stats
            </TabButton>
            <TabButton 
              active={activeTab === 'upgrades'} 
              onClick={() => setActiveTab('upgrades')}
            >
              Upgrades
            </TabButton>
          </div>
          
          {activeTab === 'stats' && renderStats()}
          {activeTab === 'upgrades' && renderUpgrades()}
        </div>
      </Modal>
    </div>
  );
};

export default GameUI;
