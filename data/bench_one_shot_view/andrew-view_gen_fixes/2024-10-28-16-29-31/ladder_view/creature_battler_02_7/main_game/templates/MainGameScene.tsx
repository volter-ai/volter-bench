import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  description: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

const CreatureDisplay = ({ creature, isPlayer, uid }: { creature: Creature; isPlayer: boolean; uid: string }) => (
  <div className={`flex flex-col items-center ${isPlayer ? 'order-1' : 'order-2'}`} key={uid}>
    <div className="text-lg font-bold">{creature.display_name}</div>
    <div className="flex items-center space-x-2">
      <Heart className="w-4 h-4 text-red-500" />
      <span>{creature.stats.hp} / {creature.stats.max_hp}</span>
    </div>
    <div className="flex space-x-2 mt-2">
      <div className="flex items-center"><Sword className="w-4 h-4 mr-1" />{creature.stats.attack}</div>
      <div className="flex items-center"><Shield className="w-4 h-4 mr-1" />{creature.stats.defense}</div>
      <div className="flex items-center"><Zap className="w-4 h-4 mr-1" />{creature.stats.speed}</div>
    </div>
  </div>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      <div className="bg-blue-500 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </div>

      <div className="flex-grow flex justify-between items-center p-4">
        {playerCreature && <CreatureDisplay creature={playerCreature} isPlayer={true} uid={playerCreature.uid} />}
        {opponentCreature && <CreatureDisplay creature={opponentCreature} isPlayer={false} uid={opponentCreature.uid} />}
      </div>

      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="mb-4 h-24 bg-gray-200 p-2 rounded">
          <p>Battle information will be displayed here.</p>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {playerCreature?.collections.skills.map((skill) => (
            <button
              key={skill.uid}
              className={`p-2 rounded ${
                availableButtonSlugs.includes(skill.display_name.toLowerCase())
                  ? 'bg-blue-500 text-white hover:bg-blue-600'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
              onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
              disabled={!availableButtonSlugs.includes(skill.display_name.toLowerCase())}
            >
              {skill.display_name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
