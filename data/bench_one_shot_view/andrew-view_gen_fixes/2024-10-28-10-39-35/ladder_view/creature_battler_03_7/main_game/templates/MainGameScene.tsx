import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  meta: {
    creature_type: string;
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

const CreatureDisplay = ({ creature, isPlayer }: { creature: Creature; isPlayer: boolean }) => (
  <div className={`flex flex-col items-center ${isPlayer ? 'order-1' : 'order-2'}`}>
    <div className="text-lg font-bold">{creature.display_name}</div>
    <div className="w-32 h-32 bg-gray-300 rounded-full mb-2"></div>
    <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
      <div 
        className="bg-blue-600 h-2.5 rounded-full" 
        style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
      ></div>
    </div>
    <div className="text-sm">{`HP: ${creature.stats.hp}/${creature.stats.max_hp}`}</div>
    <div className="flex space-x-2 mt-2">
      <span title="Attack"><Sword size={16} /> {creature.stats.attack}</span>
      <span title="Defense"><Shield size={16} /> {creature.stats.defense}</span>
      <span title="Speed"><Zap size={16} /> {creature.stats.speed}</span>
    </div>
  </div>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="flex flex-col h-screen w-full max-w-[177.78vh] mx-auto" style={{ aspectRatio: '16/9' }}>
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <div>{props.data.entities.player?.display_name || 'Player'}</div>
        <div>{props.data.entities.opponent?.display_name || 'Opponent'}</div>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-around items-center bg-green-100 p-4">
        {playerCreature ? (
          <CreatureDisplay creature={playerCreature} isPlayer={true} />
        ) : (
          <div className="text-center">Player Creature Not Available</div>
        )}
        {opponentCreature ? (
          <CreatureDisplay creature={opponentCreature} isPlayer={false} />
        ) : (
          <div className="text-center">Opponent Creature Not Available</div>
        )}
      </div>

      {/* User Interface */}
      <div className="bg-gray-100 p-4 h-1/3">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {['lick', 'tackle'].map((skillId) => {
              const skill = playerCreature?.collections?.skills?.find(s => s.meta.prototype_id === skillId);
              if (skill && availableButtonSlugs.includes(skillId)) {
                return (
                  <button
                    key={skill.uid}
                    onClick={() => emitButtonClick(skillId)}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  >
                    {skill.display_name}
                  </button>
                );
              }
              return null;
            })}
          </div>
        ) : (
          <div className="bg-white p-4 rounded shadow">
            Waiting for your turn...
          </div>
        )}
      </div>
    </div>
  );
}
