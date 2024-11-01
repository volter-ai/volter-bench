import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
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
  collections: {
    skills: Skill[];
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
  <Card className={`flex flex-col items-center p-2 ${isPlayer ? 'self-start' : 'self-end'}`}>
    <div className="text-sm font-bold">{creature.display_name}</div>
    <div className="w-20 h-20 bg-gray-300 rounded-full mb-1"></div>
    <div className="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
      <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}></div>
    </div>
    <div className="text-xs">{`HP: ${creature.stats.hp}/${creature.stats.max_hp}`}</div>
    <div className="flex space-x-1 mt-1 text-xs">
      <span title="Attack"><Sword size={12} /> {creature.stats.attack}</span>
      <span title="Defense"><Shield size={12} /> {creature.stats.defense}</span>
      <span title="Speed"><Zap size={12} /> {creature.stats.speed}</span>
    </div>
  </Card>
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
      <Card className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <div>{props.data.entities.player?.display_name}</div>
        <div>{props.data.entities.opponent?.display_name}</div>
      </Card>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center bg-green-100 p-4">
        <div className="flex-1 flex justify-center items-center">
          {playerCreature && <CreatureDisplay creature={playerCreature} isPlayer={true} />}
        </div>
        <div className="flex-1 flex justify-center items-center">
          {opponentCreature && <CreatureDisplay creature={opponentCreature} isPlayer={false} />}
        </div>
      </div>

      {/* User Interface */}
      <Card className="bg-gray-100 p-4 h-1/4 flex flex-col">
        <div className="flex-grow overflow-y-auto mb-2">
          {availableButtonSlugs.length === 0 ? (
            <div className="bg-white p-2 rounded shadow text-sm">
              Waiting for your turn...
            </div>
          ) : (
            <div className="bg-white p-2 rounded shadow text-sm">
              Choose your action:
            </div>
          )}
        </div>
        <div className="grid grid-cols-2 gap-2">
          {playerCreature?.collections?.skills?.map((skill) => (
            <button
              key={skill.uid}
              onClick={() => availableButtonSlugs.includes(skill.uid) && emitButtonClick(skill.uid)}
              className={`font-bold py-1 px-2 rounded text-sm ${
                availableButtonSlugs.includes(skill.uid)
                  ? 'bg-blue-500 hover:bg-blue-700 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            >
              {skill.display_name}
            </button>
          ))}
        </div>
      </Card>
    </div>
  );
}
