import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Heart, Swords } from 'lucide-react';

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
  description: string;
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
        {/* Player Creature */}
        <div className="w-1/3 bg-green-100 p-4 rounded-lg shadow-md">
          <h2 className="text-lg font-semibold">{playerCreature?.display_name || 'Player Creature'}</h2>
          <div className="flex items-center mt-2">
            <Heart className="text-red-500 mr-2" />
            <span>{playerCreature?.stats.hp || 0} / {playerCreature?.stats.max_hp || 0}</span>
          </div>
        </div>

        {/* Battle Indicator */}
        <div className="flex-shrink-0">
          <Swords className="text-4xl text-yellow-500" />
        </div>

        {/* Foe Creature */}
        <div className="w-1/3 bg-red-100 p-4 rounded-lg shadow-md">
          <h2 className="text-lg font-semibold">{foeCreature?.display_name || 'Foe Creature'}</h2>
          <div className="flex items-center mt-2">
            <Heart className="text-red-500 mr-2" />
            <span>{foeCreature?.stats.hp || 0} / {foeCreature?.stats.max_hp || 0}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 rounded-t-lg shadow-md">
        {availableButtonSlugs.includes('tackle') ? (
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => emitButtonClick('tackle')}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
            >
              Tackle
            </button>
          </div>
        ) : (
          <p className="text-gray-700">Waiting for your turn...</p>
        )}
      </div>
    </div>
  );
}
