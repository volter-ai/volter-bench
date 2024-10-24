import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    foe: Player;
    player_creature: Creature;
    foe_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100" style={{ aspectRatio: '16/9' }}>
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
        <CreatureCard creature={playerCreature} isPlayer={true} />
        <CreatureCard creature={foeCreature} isPlayer={false} />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 rounded-t-lg shadow-lg">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Game text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {availableButtonSlugs.includes('tackle') && (
            <button
              onClick={() => emitButtonClick('tackle')}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Tackle
            </button>
          )}
          {/* Add more buttons here as needed */}
        </div>
      </div>
    </div>
  );
}

function CreatureCard({ creature, isPlayer }: { creature: Creature | undefined; isPlayer: boolean }) {
  if (!creature) return null;

  return (
    <div className={`w-1/3 p-4 bg-white rounded-lg shadow-md ${isPlayer ? 'bg-blue-100' : 'bg-red-100'}`}>
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-lg font-bold">{creature.display_name || 'Unknown Creature'}</h2>
        {isPlayer ? <Shield className="text-blue-500" /> : <Swords className="text-red-500" />}
      </div>
      <div className="bg-gray-200 rounded-full h-4 overflow-hidden">
        <div
          className="bg-green-500 h-full"
          style={{ width: `${((creature.stats?.hp ?? 0) / (creature.stats?.max_hp ?? 1)) * 100}%` }}
        ></div>
      </div>
      <p className="mt-1 text-sm">
        HP: {creature.stats?.hp ?? 0} / {creature.stats?.max_hp ?? 0}
      </p>
    </div>
  );
}
