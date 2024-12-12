import React, { useState, useEffect } from 'react';
import { Settings, X, Users, Zap, Coins, Target, Layout } from 'lucide-react';

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
        border: '2px solid #7C45CB',
        borderRadius: '10px',
        padding: '20px',
        width: '80%',
        maxWidth: '600px',
        maxHeight: '80%',
        overflow: 'auto',
        boxShadow: '0 0 20px rgba(124, 69, 203, 0.3)',
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
            color: '#7C45CB',
            fontSize: '1.5em',
          }}>{title}</h2>
          <X
            onClick={onClose}
            style={{
              cursor: 'pointer',
              color: '#7C45CB',
            }}
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
      padding: '10px 20px',
      fontSize: '14px',
      color: '#d3d3d3',
      border: '2px solid #7C45CB',
      borderRadius: '5px',
      cursor: 'pointer',
      backgroundColor: '#2a1f3d',
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      fontFamily: 'Roboto',
      transition: 'all 0.3s ease',
      width: '100%',
    }}
    onMouseEnter={e => {
      e.target.style.backgroundColor = '#3a2f4d';
      e.target.style.boxShadow = '0 0 10px rgba(124, 69, 203, 0.5)';
    }}
    onMouseLeave={e => {
      e.target.style.backgroundColor = '#2a1f3d';
      e.target.style.boxShadow = 'none';
    }}
  >
    {Icon && <Icon size={16} />}
    <span style={{ flex: 1 }}>{children}</span>
    <span style={{ color: '#ffd700' }}>{cost} ¢</span>
  </button>
);

const HUD = ({ game }) => (
  <div style={{
    position: 'absolute',
    top: '20px',
    left: '20px',
    padding: '10px 20px',
    backgroundColor: 'rgba(26, 26, 46, 0.9)',
    color: '#d3d3d3',
    borderRadius: '10px',
    border: '2px solid #7C45CB',
    fontFamily: 'Orbitron',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      <Coins size={20} color="#ffd700" />
      <span style={{ color: '#ffd700', fontSize: '1.2em' }}>{Math.floor(game.score)}</span>
    </div>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  const [showStats, setShowStats] = useState(false);
  const [showUpgrades, setShowUpgrades] = useState(false);
  const [activeUpgradeTab, setActiveUpgradeTab] = useState('runners');

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;

  const UpgradeTab = ({ title, active, onClick }) => (
    <div
      onClick={onClick}
      style={{
        padding: '10px',
        backgroundColor: active ? '#7C45CB' : 'transparent',
        cursor: 'pointer',
        borderRadius: '5px',
        transition: 'all 0.3s ease',
      }}
    >
      {title}
    </div>
  );

  return (
    <div style={{ width: '100%', height: '100%', color: '#d3d3d3', fontFamily: 'Roboto' }}>
      <HUD game={game} />
      
      <div style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        display: 'flex',
        gap: '10px'
      }}>
        <button
          onClick={() => setShowStats(true)}
          style={{
            backgroundColor: '#2a1f3d',
            border: '2px solid #7C45CB',
            borderRadius: '5px',
            padding: '10px',
            cursor: 'pointer',
          }}
        >
          <Settings color="#7C45CB" />
        </button>
        <button
          onClick={() => setShowUpgrades(true)}
          style={{
            backgroundColor: '#2a1f3d',
            border: '2px solid #7C45CB',
            borderRadius: '5px',
            padding: '10px',
            cursor: 'pointer',
          }}
        >
          <Zap color="#7C45CB" />
        </button>
      </div>

      <Modal isOpen={showStats} onClose={() => setShowStats(false)} title="Statistics">
        <div style={{ display: 'grid', gap: '15px' }}>
          <div>Runners: {game.runnerCount}</div>
          <div>Tracks: {game.trackCount}</div>
          <div>Runner Speed: {game.runnerSpeed.toFixed(1)}</div>
          <div>Coin Spawn Rate: {game.coinSpawnRate.toFixed(1)}s</div>
          <div>Coin Value: {game.coinValue}</div>
          <div>Collection Radius: {game.collectionRadius.toFixed(1)}</div>
        </div>
      </Modal>

      <Modal isOpen={showUpgrades} onClose={() => setShowUpgrades(false)} title="Upgrades">
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          <UpgradeTab
            title="Runners"
            active={activeUpgradeTab === 'runners'}
            onClick={() => setActiveUpgradeTab('runners')}
          />
          <UpgradeTab
            title="Collection"
            active={activeUpgradeTab === 'collection'}
            onClick={() => setActiveUpgradeTab('collection')}
          />
          <UpgradeTab
            title="Tracks"
            active={activeUpgradeTab === 'tracks'}
            onClick={() => setActiveUpgradeTab('tracks')}
          />
        </div>

        {activeUpgradeTab === 'runners' && (
          <div style={{ display: 'grid', gap: '10px' }}>
            <Button onClick={() => game.upgradeRunnerSpeed()} cost={game.runnerSpeedCost} icon={Zap}>
              Upgrade Runner Speed
            </Button>
            <Button onClick={() => game.upgradeRunnerCount()} cost={game.runnerCountCost} icon={Users}>
              Add Runner
            </Button>
          </div>
        )}

        {activeUpgradeTab === 'collection' && (
          <div style={{ display: 'grid', gap: '10px' }}>
            <Button onClick={() => game.upgradeCoinSpawnRate()} cost={game.coinSpawnRateCost} icon={Coins}>
              Upgrade Coin Spawn Rate
            </Button>
            <Button onClick={() => game.upgradeCoinValue()} cost={game.coinValueCost} icon={Coins}>
              Increase Coin Value
            </Button>
            <Button onClick={() => game.upgradeCollectionRadius()} cost={game.collectionRadiusCost} icon={Target}>
              Increase Collection Radius
            </Button>
          </div>
        )}

        {activeUpgradeTab === 'tracks' && (
          <div style={{ display: 'grid', gap: '10px' }}>
            <Button onClick={() => game.upgradeTrackCount()} cost={game.trackCountCost} icon={Layout}>
              Add Track
            </Button>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default GameUI;
